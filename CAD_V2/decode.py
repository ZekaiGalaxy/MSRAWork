import pickle
import json
from tqdm import tqdm
import torch
import os
import trimesh
import numpy as np
import json

# def load_pkl(file_path):
#     with open(file_path, "rb") as file:
#         return pickle.load(file)

# x = load_pkl("/f_ndata/zekai/zecheng_cad/02747177.pkl")
# print(x[0])

def load_json(path):
    with open(path, "r") as file:
        return json.load(file)

x = load_json("/root/taxonomy.json")

cnt = 0
for xx in x:
    cnt += xx['numInstances']
print(cnt)


# print(find_obj_name("03001627"))

# def get_3d_data(file_path): 
#     mesh = trimesh.load(file_path, force='mesh')
#     vertices = mesh.vertices
#     faces = mesh.faces  
#     return faces

# def count_f_lines(file_path):
#     count = 0
#     with open(file_path, 'r') as file:
#         for line in file:
#             if line.startswith('f'):
#                 count += 1
#     return count

# def count_ranges_in_list(lengths, range_size, max_value):
#     range_counts = {f"{i}-{i + range_size - 1}": 0 for i in range(0, max_value, range_size)}
#     for length in lengths:
#         for range_start in range(0, max_value, range_size):
#             if range_start <= length < range_start + range_size:
#                 range_counts[f"{range_start}-{range_start + range_size - 1}"] += 1
#                 break
#     return range_counts


# faces_len = []
# directory = "/f_ndata/zekai/ShapeNetCore.v2/04379243"
# for checklist in tqdm(os.listdir(directory)[:2000]):  
#     for filename in os.listdir(os.path.join(directory, checklist,'models')):
#         if (filename.endswith(".obj") or  filename.endswith(".glb") or  filename.endswith(".off")):
#             file_path = os.path.join(directory, checklist,'models',filename)
#             # faces = get_3d_data(file_path) 
#             # faces = open(file_path, 'r').readlines()[-1]
#             # print(faces)
#             faces_len.append(count_f_lines(file_path))

# counts = count_ranges_in_list(faces_len, 100, 2000)
# print(counts)