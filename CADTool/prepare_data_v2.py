from obj2code import *
from tokenizer import tokenize
import pickle
from tqdm import tqdm
# read a file, convert to code
# we dont want to remove all the file that have the same points because we just want to sample from model.

def read_list(path):
    with open(path, 'r') as f:
        data = f.read()
        return data.strip().split('\n')

def save_list_to_pkl(data, file_path):
    # Open the file in binary write mode
    with open(file_path, 'wb') as file:
        # Use pickle to dump the data into the file
        pickle.dump(data, file)

def load_data_from_pkl(file_path):
    # Open the file in binary read mode
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

def analyze_code_len(data, maxlen=512):
    count_below = sum(1 for d in data if d[2] < maxlen)
    percentage = (count_below / len(data)) * 100
    return percentage

def save_list_to_file(list_of_elements, file_path):
    # Open the file at 'file_path' in write mode ('w')
    with open(file_path, 'w') as file:
        # Iterate over the elements and write each as a new line in the file
        for element in list_of_elements:
            file.write(str(element) + "\n")  # Convert the element to string in case it isn't

def read_obj(path):
    obj_data = load_obj(path)
    vertexs, curves = obj_data.split('\n')[1:3]
    vlen = int(vertexs.split(': ')[-1])
    clen = int(curves.split(': ')[-1])
    # print(clen, vlen)
    code_data = obj2code(obj_data)
    # print("Code Data")
    # print(code_data)
    code_len = tokenize(code_data)
    return code_data, code_len
    # if code_len <= 500:

    # print(vlen,clen,code_len)
    # return (vlen,clen,code_len)

# read_obj('/f_ndata/zekai/data/cad_norm/0001/00010008/00010008_002_param.obj')

def convert_to_code():
    data = []
    obj_path = read_list('output.txt')
    for x in tqdm(obj_path):
        code_data, code_len = read_obj(x)
        if code_len < 500:
            data.append(code_data.replace('\n','\\n'))
    save_list_to_file(data, '/f_ndata/zekai/data/cad_data.txt')
convert_to_code()

# codes = read_list('/f_ndata/zekai/data/cad_data.txt')
# for x in codes:
#     print(x.replace('\\n','\n'))
#     print('#'*20)

# 512

# def check_tokenized_length():
#     length_data = []
#     obj_path = read_list('output.txt')[:10000]
#     for x in tqdm(obj_path):
#         length_data.append(read_obj(x))
#     save_list_to_pkl(length_data, 'length_analysis.pkl')

# check_tokenized_length()

# length_data = load_data_from_pkl('length_analysis.pkl')
# for maxlen in [128,256,512,1024,2048]:
#     p = analyze_code_len(length_data, maxlen)
#     print(f"Percentage of code_len below {maxlen}: {p:.2f}%")


