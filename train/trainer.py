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
