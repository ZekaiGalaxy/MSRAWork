import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Input Path')
parser.add_argument('--input_path', type=str, help='Input Path')
args = parser.parse_args()

input_file = '.'.join(args.input_path.split('.')[:-1])
input_folder = 'test/'+input_file
print("Input File:", input_file)
os.makedirs(input_folder, exist_ok=True)
subprocess.run(['python', 'load_inference.py','--input_path',input_file])
subprocess.run(['python', 'code2obj.py','--input_folder',input_folder])
subprocess.run(['python', 'compile_obj.py', '--data_folder', input_folder])

print('Done!')