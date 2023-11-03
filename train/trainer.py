from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import load_dataset
import pandas as pd

# Step 1: Load Dataset
# Replace 'your_dataset.csv' with your dataset file
dataset = pd.read_csv('your_dataset.csv')
dataset = load_dataset('csv', data_files='your_dataset.csv')

# Step 2: Load Tokenizer and Model
# Replace 'llama-model-name' with the specific LLaMA model you want to use
model_name = 'llama-model-name'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)  # Adjust num_labels as per your task

# Step 3: Preprocess Data
def preprocess_function(examples):
    return tokenizer(examples['text'], truncation=True, padding=True)

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Step 4: Create Training Arguments
training_args = TrainingArguments(
    output_dir='./results',          
    num_train_epochs=3,              
    per_device_train_batch_size=16,  
    per_device_eval_batch_size=64,   
    warmup_steps=500,                
    weight_decay=0.01,               
    logging_dir='./logs',            
    logging_steps=10,
)

# Step 5: Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    eval_dataset=tokenized_dataset['test'],
)

# Step 6: Fine-tune the Model
trainer.train()



from transformers import LlamaForCausalLM, LlamaTokenizer, Trainer, TrainingArguments
import torch
from datasets import load_dataset

# Step 1: Loading the Model
model_name = "/share2/wangyq/resources/models/Llama-2-7b-hf"  # Replace with the actual model name if different
tokenizer = LlamaTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = LlamaForCausalLM.from_pretrained(model_name)

# Step 2: Data Preparation
dataset = load_dataset('text', data_files='svg_data.txt')
def tokenize_function(examples):
    tokenized_inputs = tokenizer(examples["text"], padding=True, truncation=True)
    # Shift the token IDs to the right to create labels
    tokenized_inputs["labels"] = tokenized_inputs["input_ids"].copy()
    return tokenized_inputs
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# # Step 3: Training
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,              # Set number of epochs according to your needs
    per_device_train_batch_size=1,   # Adjust batch size according to your GPU
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
)

trainer.train()

# # Step 4: Text Generation
prompt = "Your text prompt here"  # Replace with your starting text
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(inputs.input_ids, max_length=50, temperature=0.5)
print(tokenizer.decode(outputs[0]))
