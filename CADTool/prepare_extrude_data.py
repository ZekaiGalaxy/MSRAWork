from tokenizer import tokenize
import pickle
from tqdm import tqdm
from cad_utils import *
from cad_converter import *
import os

x = load_jsonl("/f_ndata/zekai/data/cad_extrude_data_ori_mask.jsonl")

import random
import re

random.seed(0)

def mask_numbers(text, mask_ratio=0.7):
    # Function to decide whether to mask a number or not
    def mask_or_not(match):
        return '<mask>' if random.random() < mask_ratio else match.group()

    # Regular expression to replace numbers with '<mask>' based on the mask ratio
    masked_text = re.sub(r'-?\d+', mask_or_not, text)
    return masked_text

# iterate x, if len > 1024 then continue, else add {'input': masked_text_70_percent, 'labels': xx['labels']} to new_x
# save the new_x to /f_ndata/zekai/data/cad_extrude_data_ori_mask_70_test.jsonl
# Code here
new_x = []
for xx in tqdm(x):
    if len(xx['labels']) > 1024:
        continue
    
    text = xx['labels']
    masked_text_70_percent = mask_numbers(text, mask_ratio=0.3)
    new_x.append({'input': masked_text_70_percent, 'labels': xx['labels']})

print(len(new_x))

save_jsonl(new_x, "/f_ndata/zekai/data/cad_extrude_data_ori_mask_30_test.jsonl")

# for xx in tqdm(new_x):
#     print(xx['input'])
#     print('*'*20)
#     print(xx['labels'])
#     print('='*20)