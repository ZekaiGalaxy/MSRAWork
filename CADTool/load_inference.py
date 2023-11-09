import json
import os
import cad_utils
import argparse

parser = argparse.ArgumentParser(description='Input File.')
parser.add_argument('--input_path', type=str, help='the path to the input file')
args = parser.parse_args()

cad_data = cad_utils.load_jsonl(f'/f_ndata/zekai/inference_jsonl/{args.input_path}.jsonl')[0]
print(len(cad_data['case']))
base_path = f'/workspace/MSRAWork/CADTool/test/{args.input_path}'
for i in range(len(cad_data['case'])):
    cad_code = cad_data['case'][i].replace('<unk>','').replace('<s>','').strip()
    folder_name = os.path.join(base_path, f'{i+1:04d}')
    file_name = os.path.join(folder_name, f'{i+1:04d}.code')
    cad_utils.save_text(cad_code, file_name)