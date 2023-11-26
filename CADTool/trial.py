import os

def count_folders_with_stl_files(path):
    folder_count = 0
    all_cnt = 0
    for root, dirs, files in os.walk(path):
        all_cnt += 1
        if any(file.endswith('.stl') for file in files):
            folder_count += 1

    return folder_count, all_cnt

for x in os.listdir("/workspace/MSRAWork/CADTool/test"):
    if os.path.isdir(os.path.join("/workspace/MSRAWork/CADTool/test",x)) and x.startswith("Ori"):
        p = os.path.join("/workspace/MSRAWork/CADTool/test",x)
        path_to_search = p
        count, all_cnt = count_folders_with_stl_files(path_to_search)
        print(f"{count}/{all_cnt}={round(count/all_cnt*100,0)}")
