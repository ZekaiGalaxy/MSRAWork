# load pkl to list
import pickle
import os
def read_pkl(path):
    with open(path, "rb") as file:
        return pickle.load(file)
# merge the list
all = []
dir = "/f_ndata/zekai/zecheng_cad"
for p in os.listdir(dir):
    path = os.path.join(dir, p)
    all += read_pkl(path)

print(len(all))

# save the list to all.pkl
save_path = "/f_ndata/zekai/zecheng_cad/all.pkl"
with open(save_path, "wb") as file:
    pickle.dump(all, file)