import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm
import json
import argparse

parser = argparse.ArgumentParser(description='Process some integers and a float.')
parser.add_argument('--t', type=float, default=1.0, help='A float')
parser.add_argument('--mask', type=int, default=70, help='A float')
args = parser.parse_args()

def setup_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained("/zecheng/model_hub/CodeLlama-7b-hf")
    tokenizer.pad_token_id = tokenizer.unk_token_id
    # special_tokens = ["<face>","</face>","<loop>","</loop>",'type="outer"','type="inner"','<Line>','<Arc>','<Cricle>','<height>']
    # for i in range(30):
    #     special_tokens.append(f"<node{i}>")
    special_tokens = [' <mask>','<unmask>']
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
                max_length=2048,
                num_return_sequences=1,
                do_sample=True,
                temperature=temperature,
                use_cache=True,
            )
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=False)
            generated_text = generated_text.split('<unmask>')[1].strip()
            generated_text = generated_text.replace('<unk>', '').replace('<s>', '').strip()
            # generated_texts.append(generated_text)

            # now append the generated_text to the end of a file

            with open(f"/f_ndata/zekai/inference_jsonl/Ori_mask_{args.mask}_{args.t}.txt", 'a+') as f:
                f.write(generated_text+'\n')
                f.write('*'*20+'\n')
                f.flush()

            pbar.update(1)
    return generated_texts

# Example usage:
model_name = "/zecheng/svg_model_hub/CAD_CodeLLaMA-7b_Mask_Ori/"  # Replace with the actual model name
model, tokenizer = setup_model(model_name)

def load_jsonl(path):
    data = []
    with open(path, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

data = load_jsonl(f"/f_ndata/zekai/data/cad_extrude_data_ori_mask_{args.mask}_test.jsonl")
prompts = []
for i in range(len(data)):
    prompts.append(data[i]['input']+'\n<unmask>')

temperature = args.t 
generate_text(prompts, model, tokenizer, temperature)

# res.append({"case": generated_texts})
# save_jsonl(res, "/workspace/zecheng/SUWA/zekai/generated_res.jsonl")
# for i, text in enumerate(generated_texts):
#     print(f"Generated text {i+1}:\n{text}\n")
