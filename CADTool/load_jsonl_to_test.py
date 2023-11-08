import json
import os

def read_jsonl(path):
    data = []
    with open(path, 'r') as jsonl_file:
        for line in jsonl_file:
            data.append(json.loads(line.strip()))
    return data

# /workspace/SUWA/zekai/_0_0.7.jsonl,/workspace/SUWA/zekai/checkpoint-200_0_0.7.jsonl,/workspace/SUWA/zekai/checkpoint-300_0_0.7.jsonl
cad_data = read_jsonl('/workspace/SUWA/zekai/checkpoint-300_0_0.7.jsonl')[0]
print(len(cad_data['case']))
base_path = '/workspace/MSRAWork/CADTool/test2'
for i in range(128):
    cad_code = cad_data['case'][i].replace('<unk>','').replace('<s>','').strip()

    folder_name = os.path.join(base_path, f'{i+1:04d}')
    file_name = os.path.join(folder_name, f'{i+1:04d}.code')
    os.makedirs(folder_name, exist_ok=True)
    with open(file_name, 'w') as code_file:
        code_file.write(cad_code)