import json
import os

def read_jsonl(path):
    data = []
    with open(path, 'r') as jsonl_file:
        for line in jsonl_file:
            data.append(json.loads(line.strip()))
    return data

cad_data = read_jsonl('/workspace/SUWA/zekai/generated_res.jsonl')[0]
base_path = '/workspace/MSRAWork/CADTool/test'
for i in range(128):
    cad_code = cad_data['case'][i].replace('<unk>','').replace('<s>','').strip()

    folder_name = os.path.join(base_path, f'{i+1:04d}')
    file_name = os.path.join(folder_name, f'{i+1:04d}.code')
    os.makedirs(folder_name, exist_ok=True)
    with open(file_name, 'w') as code_file:
        code_file.write(cad_code)