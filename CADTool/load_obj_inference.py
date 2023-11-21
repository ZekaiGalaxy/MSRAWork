import json
import os
import cad_utils
import argparse
import cad_converter

def split_extrude(text):
    parts = text.split("# Extrude Operation:")
    ans = ["# WaveFront *.obj file\n# Extrude Operation:"+x for x in parts[1:]]
    return ans

parser = argparse.ArgumentParser(description='Input File.')
parser.add_argument('--input_path', type=str, help='the path to the input file', default='Ori_model_32_0.7_0')
args = parser.parse_args()

cad_data = cad_utils.load_jsonl(f'/f_ndata/zekai/inference_jsonl/{args.input_path}.jsonl')[0]
print(len(cad_data['case']))
base_path = f'/workspace/MSRAWork/CADTool/test/{args.input_path}'
for i in range(len(cad_data['case'])):
    try:
        cad_obj = cad_data['case'][i]
        cad_objs = split_extrude(cad_obj)
        for idx,cad_obj in enumerate(cad_objs):
            cad_json = cad_converter.obj2json(cad_obj,quantize=True) 
            cad_json = cad_converter.extrude_format_json(cad_json)
            formatted_cad_obj = cad_converter.json2obj(cad_json)
            folder_name = os.path.join(base_path, f'{i+1:04d}')
            file_name = os.path.join(folder_name, f'{idx+1:04d}.obj')
            cad_utils.save_text(formatted_cad_obj, file_name)
    except:
        pass