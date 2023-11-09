from tokenizer import tokenize
import pickle
from tqdm import tqdm
import cad_utils
import cad_converter

# process paths
x = cad_utils.find_obj_files('/f_ndata/zekai/data/cad_norm')
cad_utils.save_list_to_file(x, '/f_ndata/zekai/data/cad_norm_files.txt')

# obj -> code (cad_data.txt)
def read_obj(path):
    obj_data = cad_utils.load_text(path)
    vertexs, curves = obj_data.split('\n')[1:3]
    vlen = int(vertexs.split(': ')[-1])
    clen = int(curves.split(': ')[-1])
    code_data = cad_converter.obj2code(obj_data)
    code_len = tokenize(code_data)
    return code_data, code_len

def convert_to_code():
    data = []
    obj_path = cad_utils.load_lst('/f_ndata/zekai/data/cad_norm_files.txt')
    for x in tqdm(obj_path):
        code_data, code_len = cad_utils.read_text(x)
        if code_len < 500:
            data.append(code_data.replace('\n','\\n'))
    cad_utils.save_lst(data, '/f_ndata/zekai/data/cad_data.txt')

convert_to_code()

def print_code():
    codes = cad_utils.load_lst('/f_ndata/zekai/data/cad_data.txt')
    for x in codes:
        print(x.replace('\\n','\n'))
        print('#'*20)

# 512

def check_tokenized_length():
    def analyze_code_len(data, maxlen=512):
        count_below = sum(1 for d in data if d[2] < maxlen)
        percentage = (count_below / len(data)) * 100
        return percentage
    length_data = []
    obj_path = cad_utils.load_lst('output.txt')[:10000]
    for x in tqdm(obj_path):
        length_data.append(read_obj(x))
    cad_utils.save_pkl(length_data, '/f_ndata/zekai/data/length_analysis.pkl')

    length_data = cad_utils.load_pkl('/f_ndata/zekai/data/length_analysis.pkl')
    for maxlen in [128,256,512,1024,2048]:
        p = analyze_code_len(length_data, maxlen)
        print(f"Percentage of code_len below {maxlen}: {p:.2f}%")

# check_tokenized_length()




