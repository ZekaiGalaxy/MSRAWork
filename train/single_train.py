from transformers import LlamaForCausalLM, LlamaTokenizer, Trainer, TrainingArguments
import torch
from datasets import load_dataset

# Step 1: Loading the Model
model_name = "/f_ndata/zekai/models/CodeLlama-7b-hf"  # Replace with the actual model name if different
tokenizer = LlamaTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = LlamaForCausalLM.from_pretrained(model_name)