import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def setup_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer

def generate_text(prompts, model, tokenizer, temperature=1.0):
    generated_texts = []
    for prompt in prompts:
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = model.generate(
            inputs,
            max_length=512,
            num_return_sequences=1,
            do_sample=True,
            temperature=temperature
        )
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        generated_texts.append(generated_text)
    return generated_texts

# Example usage:
model_name = "/f_ndata/zekai/models/CodeLlama-7b-hf"  # Replace with the actual model name
model, tokenizer = setup_model(model_name)
prompts = [""]*16 # Replace with your actual prompts
temperature = 0.7  # You can adjust the temperature as needed

generated_texts = generate_text(prompts, model, tokenizer, temperature)
for i, text in enumerate(generated_texts):
    print(f"Generated text {i+1}:\n{text}\n")
