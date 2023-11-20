import os
from tqdm import tqdm
import json, pickle

def make_dir(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_lst(data, path):
    make_dir(path)
    with open(path, 'w') as f:
        for d in data:
            f.write(str(d) + "\n")  

def load_lst(path):
    with open(path, 'r') as f:
        return f.read().strip().split('\n')

def save_pkl(data, path):
    make_dir(path)
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def load_pkl(data, path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def save_json(data, path):
    make_dir(path)
    with open(path, 'w') as f:
        json.dump(data, f)

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_text(data, path):
    make_dir(path)
    with open(path, 'w') as f:
        f.write(data)

def load_text(path):
    with open(path, 'r') as f:
        return f.read()

def save_jsonl(data, path):
    make_dir(path)
    with open(path, 'w+') as f:
        for d in data:
            json.dump(d, f)
            f.write('\n')

def load_jsonl(path):
    data = []
    with open(path, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

def checkp(name, data):
    print('='*20+' '+name+' '+'='*20)
    print(data)
    print('')

def find_file_with_pattern(folder_path, p):
    obj_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(p):
                obj_files.append(os.path.join(root, file))
    return obj_files

def find_obj_files(start_path):
    obj_files = []
    for entry in tqdm(os.listdir(start_path)):
        entry_path = os.path.join(start_path, entry)
        if os.path.isdir(entry_path):
            for inner_entry in os.listdir(entry_path):
                inner_entry_path = os.path.join(entry_path, inner_entry)
                for file in os.listdir(inner_entry_path):
                    obj_files.append(os.path.join(inner_entry_path,file))
    
    return obj_files