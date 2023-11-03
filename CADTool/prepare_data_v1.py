import os
from tqdm import tqdm
# find all file under a folder with .obj
def find_file_with_pattern(folder_path, p):
    obj_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(p):
                obj_files.append(os.path.join(root, file))
    return obj_files

def find_obj_files(start_path):
    obj_files = []
    # List all entries in the start_path
    for entry in tqdm(os.listdir(start_path)):
        entry_path = os.path.join(start_path, entry)
        # If the entry is a directory, list its contents
        if os.path.isdir(entry_path):
            for inner_entry in os.listdir(entry_path):
                inner_entry_path = os.path.join(entry_path, inner_entry)
                for file in os.listdir(inner_entry_path):
                    obj_files.append(os.path.join(inner_entry_path,file))
    
    return obj_files

x = find_obj_files('/f_ndata/zekai/data/cad_norm')

def save_list_to_file(list_of_elements, file_path):
    # Open the file at 'file_path' in write mode ('w')
    with open(file_path, 'w') as file:
        # Iterate over the elements and write each as a new line in the file
        for element in list_of_elements:
            file.write(str(element) + "\n")  # Convert the element to string in case it isn't

save_list_to_file(x, 'output.txt')

