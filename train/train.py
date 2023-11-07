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
import deepspeed
deepspeed.ops.op_builder.CPUAdamBuilder().load()

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

class CADDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.tokenizer = tokenizer
        self.dataset = data

    def __len__(self):
        return len(self.dataset)
    
    def __getitem__(self, idx):
        cad_code = [self.dataset[x] for x in idx]
        seq_inputs = self.tokenizer(
            cad_code, 
            padding="max_length", 
            truncation=True, 
            max_length=512,
            return_tensors="pt",
        )
        seq_input_ids = seq_inputs.input_ids
        seq_attention_mask = seq_inputs.attention_mask
        labels = seq_input_ids.clone()
        return {
            "input_ids": seq_input_ids,
            "attention_mask": seq_attention_mask,
            "labels": labels
        }
        
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
    tokenizer.pad_token_id = tokenizer.unk_token_id

    data = load_text(data_args.data_path)
    data = [x.replace('\\n','\n') for x in data]
    # for i in range(5):
    #     x = data[i]['text']
    #     print(tokenizer.tokenize(x))  
    #     print(len(tokenizer.tokenize(x)))
    #     print("*"*50)
    
    dataset = CADDataset(data, tokenizer)

    # def tokenize_function(examples):
    #     print("examples")
    #     print(len(examples["text"]))
    #     print(examples["text"][0])
    #     tokenized_inputs = tokenizer(examples["text"],             padding="max_length", 
    #         truncation=True, 
    #         max_length=self.max_seq_len,
    #         return_tensors="pt",
    #     max_length=512, truncation=True, padding="longest")
    #     # print(tokenized_inputs)
    #     # print(tokenized_inputs["input_ids"])
    #     # tokenized_inputs["labels"] = tokenized_inputs["input_ids"].clone()
    #     # print(tokenized_inputs["labels"])
    #     return tokenized_inputs
    
    # dataset = Dataset.from_dict({'text': [item['text'] for item in dataset]})
    # tokenized_dataset = dataset.map(tokenize_function, batched=True)
    # data_collator = DataCollatorForLanguageModeling(
    #     tokenizer=tokenizer, mlm=False  # For standard language modeling; mlm=True is for masked language modeling (e.g., BERT)
    # )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
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
