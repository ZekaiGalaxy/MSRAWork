from cad_utils import *
# load /f_ndata/zekai/data/cad_extrude_data_ori_mask.jsonl and print first one


text = """# WaveFront *.obj file
# Extrude Operation: New

v 2 -5 
v 191  <mask>

face
out
c 0 1 

Extrude 0 25  
T_origin 0 0 0 
T_xaxis 1  <mask> 0 
T_yaxis 0  <mask> 0 
T_zaxis 0 0 1 
<unmask> # WaveFront *.obj file
# Extrude Operation: New

v 2 9 
v 191 1 

face
out
c 1 2 

Extrude -25 25  
T_origin 1 1 1 
T_xaxis 1 2 1 
T_yaxis 1 1 2 
T_zaxis 2 1 1
"""

x = 
print(x)