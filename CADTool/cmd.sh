# obj -> stp
# stp -> render
conda activate cad37
python obj2code.py
python obj2step.py --data_folder example_obj
python render.py  --input_dir example_obj --output_dir example_img
python obj2step.py --data_folder formatted_obj
python render.py  --input_dir formatted_obj --output_dir formatted_img

# under utils
# parse DeepCAD json to a simple obj format 
python convert.py --data_folder /f_ndata/zekai/data/cad_json --output_folder /f_ndata/zekai/data/cad_obj

# normalize CAD and update the obj file
python normalize.py --data_folder /f_ndata/zekai/data/cad_obj --out_folder /f_ndata/zekai/data/cad_norm

/f_ndata/zekai/data/cad_norm



# sometimes rounding can lead to same point location!
# We should discard these data!
python load_jsonl_to_test.py
python code2img.py
python obj2step.py --data_folder test4