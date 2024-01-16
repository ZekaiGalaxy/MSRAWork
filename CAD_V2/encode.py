from tqdm import tqdm
import torch
import os
import trimesh
import numpy as np
import json
import pickle

def load_json(path):
    with open(path, "r") as file:
        return json.load(file)

x = load_json("/root/taxonomy.json")

def save_pkl(data, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(data, file)

def find_obj_name(name):
    for i in x:
        if i["synsetId"] == name:
            return i["name"]
    return ""

def quantize(v):
    return torch.round(v * 128) + 128

def link(vertices, faces):
    new_faces = torch.zeros((faces.size(0), 9), dtype=torch.int64)
    for i, face in enumerate(faces):
        new_faces[i] = torch.cat([vertices[face[0]],
                                vertices[face[1]],
                                vertices[face[2]]])
    return new_faces

def write_obj(vertices, faces, file_path):
    with open(file_path, "w") as file:
        for vertex in vertices:
            file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            file.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")

def decode_faces(new_faces):
    num_vertices = new_faces.size(0) * 3
    decoded_vertices = torch.zeros((num_vertices, 3), dtype=torch.float32)
    for i in range(new_faces.size(0)):
        for j in range(3):
            decoded_vertices[i * 3 + j] = new_faces[i, j * 3:(j + 1) * 3]
    unique_vertices, inverse_indices = torch.unique(decoded_vertices, dim=0, return_inverse=True)
    dequantized_vertices = (unique_vertices - 128) / 128.0
    decoded_faces = inverse_indices.view(-1, 3)

    return dequantized_vertices, decoded_faces

def get_3d_data(file_path): 
    mesh = trimesh.load(file_path, force='mesh')
    vertices = mesh.vertices
    faces = mesh.faces   
    # centered
    centered_vertices = vertices - np.mean(vertices, axis=0)
    # normalize to unit length
    max_abs = np.max(np.abs(centered_vertices))
    vertices_normalized = centered_vertices / (max_abs / 0.95)  
    # sort vertices: y, x, z
    vertices_sorted_indices = np.lexsort((vertices_normalized[:, 1], vertices_normalized[:, 0], vertices_normalized[:, 2]))
    vertices_normalized_sorted = vertices_normalized[vertices_sorted_indices]
    # Convert indices to tuples for creating Look-Up Table (LUT)
    tuples_sorted_indices = [tuple([index]) for index in vertices_sorted_indices.tolist()]
    # Create Look-Up Table (LUT)
    lut = {old_index[0]: new_index for new_index, old_index in enumerate(tuples_sorted_indices)}
    # Reindex faces using LUT
    faces_reindexed = np.vectorize(lut.get, otypes=[int])(faces) 
    # sort faces based on their lowest vertex index
    faces_sorted = faces_reindexed[np.lexsort(faces_reindexed.T)]

    vertices, faces = torch.tensor(vertices_normalized_sorted), torch.tensor(faces_sorted)
    vertices = quantize(vertices)
    faces = link(vertices, faces)
    
    return vertices, faces

def load_models(directory):
    obj_datas = []  
    for checklist in tqdm(os.listdir(directory)):  
        for filename in os.listdir(os.path.join(directory, checklist,'models')):
            if (filename.endswith(".obj") or  filename.endswith(".glb") or  filename.endswith(".off")):
                file_path = os.path.join(directory, checklist,'models',filename)
                vertices, faces = get_3d_data(file_path) 
                if faces.shape[0] > 2048:
                    continue

                json_data = {
                    'keywords': [find_obj_name(directory.split('/')[-1])],
                    'mesh_data': faces
                }
                obj_datas.append(json_data)
    
    save_pkl(obj_datas, f"/f_ndata/zekai/zecheng_cad/{directory.split('/')[-1]}.pkl")
    return obj_datas

def pipeline(path):
    # load obj, quantize, link, decode, dequantize, write obj
    vertices, faces = get_3d_data(path)
    dequantized_vertices, decoded_faces = decode_faces(faces)
    write_obj(dequantized_vertices, decoded_faces, f'{path}.obj')

# for d in sorted(os.listdir("/f_ndata/zekai/ShapeNetCore.v2")):
#     if d < "03001627_processed":
#         print('skip', d)
#         continue
#     try:
#         if os.path.isdir(os.path.join("/f_ndata/zekai/ShapeNetCore.v2", d)):
#             load_models(f"/f_ndata/zekai/ShapeNetCore.v2/{d}")
#     except:
#         pass

import pickle
def load_pkl(path):
    with open(path, "rb") as f:
        return pickle.load(f)

path = "/f_ndata/zekai/compress_level_1_predictions.pkl"

x = load_pkl(path)

# 200

pred = x['raw_predict']
label = x['golden']

for i in tqdm(range(200)):
    faces = pred[i].squeeze(0)
    dequantized_vertices, decoded_faces = decode_faces(faces)
    write_obj(dequantized_vertices, decoded_faces, f'/f_ndata/zekai/zecheng_results/pred{i}.obj')

    faces = label[i].squeeze(0)
    dequantized_vertices, decoded_faces = decode_faces(faces)
    write_obj(dequantized_vertices, decoded_faces, f'/f_ndata/zekai/zecheng_results/label{i}.obj')

