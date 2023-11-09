# load jsonl -> test

python load_inference.py --input_file
python code2obj.py --input_folder
python compile_obj.py --data_folder --input_folder

write the python code:

using parser to get:
input_path = 'xxx.jsonl'
make a dir called
test/xxx
bash 'python load_jsonl_to_test.py'
bash 'python code2img.py'
bash 'python obj2step.py --data_folder test/xxx'

checkpoint-200_0_0.5.jsonl

import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Input Path')
parser.add_argument('input_path', type=str, help='Input Path')
args = parser.parse_args()

input_file = args.input_path.split('.')[0]
input_folder = 'test/'+input_file
os.makedirs(input_folder, exist_ok=True)
subprocess.run(['python', 'load_inference.py','--input_file',input_file])
subprocess.run(['python', 'code2obj.py','--input_folder',input_folder])
subprocess.run(['python', 'compile_obj.py', '--data_folder', input_folder])

print('Done!')