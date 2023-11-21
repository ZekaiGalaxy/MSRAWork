import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm
import json
import argparse

parser = argparse.ArgumentParser(description='Process some integers and a float.')
parser.add_argument('--idx', type=int, default=0, help='An integer')
parser.add_argument('--t', type=float, default=1.0, help='A float')
args = parser.parse_args()

def save_jsonl(data, file_path):
    with open(file_path, 'w+', encoding='utf-8') as file:
        for record in data:
            json_record = json.dumps(record)
            file.write(json_record + '\n')

def setup_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained("/zecheng/model_hub/CodeLlama-7b-hf")
    tokenizer.pad_token_id = tokenizer.unk_token_id
    special_tokens = []
    for i in range(201):
        special_tokens.append(f" {i}")
        special_tokens.append(f" -{i}")

    tokenizer.add_tokens(special_tokens,special_tokens=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
    model.eval()
    model.half()
    return model, tokenizer

def generate_text(prompts, model, tokenizer, temperature=1.0):
    generated_texts = []
    with tqdm(total=len(prompts), desc="Generating text") as pbar:
        for prompt in prompts:
            inputs = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(
                inputs,
                max_length=1024,
                num_return_sequences=1,
                do_sample=True,
                temperature=temperature,
                use_cache=True,
            )
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=False)
            generated_text = generated_text.replace('<unk>', '').replace('<s>', '').strip()
            generated_texts.append(generated_text)
            pbar.update(1)
    return generated_texts

# Example usage:
model_name = "/zecheng/svg_model_hub/CAD_CodeLLaMA-7b_Ori/"  # Replace with the actual model name
model, tokenizer = setup_model(model_name)
prompts = [""]*32 # Replace with your actual prompts
temperature = args.t  # You can adjust the temperature as needed

res = []
generated_texts = generate_text(prompts, model, tokenizer, temperature)
res.append({"case": generated_texts})
save_jsonl(res, f"/f_ndata/zekai/inference_jsonl/Ori_model_32_{args.t}_{args.idx}.jsonl")
