import sys
import copy
import random
from dataclasses import dataclass, field
from typing import Optional, Dict, Sequence
import os
import torch
import torch.distributed
import transformers
from transformers import Trainer, DataCollatorForLanguageModeling
from datasets import Dataset
import os

@dataclass
class ModelArguments:
    model_name_or_path: Optional[str] = field(default="facebook/opt-125m")

@dataclass
class DataArguments:
    data_path: str = field(default=None, metadata={"help": "Path to the training data."})

@dataclass
class TrainingArguments(transformers.TrainingArguments):
    cache_dir: Optional[str] = field(default=None)

def load_text(path):
    with open(path, 'r') as f:
        data = f.read()
        return data.strip().split('\n')
        
def train():
    parser = transformers.HfArgumentParser((ModelArguments, DataArguments, TrainingArguments))
    model_args, data_args, training_args = parser.parse_args_into_dataclasses()
        
    model = transformers.AutoModelForCausalLM.from_pretrained(
        model_args.model_name_or_path,
        cache_dir=training_args.cache_dir,
    )
    model.config.pad_token_id = model.config.eos_token_id

    tokenizer = transformers.AutoTokenizer.from_pretrained(
        model_args.model_name_or_path,
        cache_dir=training_args.cache_dir,
        padding_side="right",
        use_fast=True,
    )

    special_tokens = ["<face>","</face>","<loop>","</loop>",'type="outer"','type="inner"','<Line>','<Arc>','<Cricle>','<height>']
    for i in range(30):
        special_tokens.append(f"<node{i}>")
    for i in range(201):
        special_tokens.append(f"{i}")
        special_tokens.append(f"-{i}")
    tokenizer.add_tokens(special_tokens,special_tokens=True)
    model.resize_token_embeddings(len(tokenizer))
    tokenizer.pad_token_id = 0

    data = load_text(data_args.data_path)
    data = [{'text':x.replace('\\n','\n')} for x in data]

    def tokenize_function(prompt):
        result = tokenizer(
            prompt['text'],
            truncation=True,
            max_length=512,
            padding=False,
            return_tensors=None,
        )
        result["labels"] = result["input_ids"].copy()
        return result
    
    dataset = Dataset.from_dict({'text': [item['text'] for item in data]})
    tokenized_dataset = dataset.map(tokenize_function)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )
    model.config.use_cache = False
    model.is_parallelizable = True
    model.model_parallel = True
    trainer.train()
    trainer.save_model(training_args.output_dir)
    tokenizer.save_pretrained(training_args.output_dir)
    model.config.save_pretrained(training_args.output_dir)


if __name__ == "__main__":
    train()
