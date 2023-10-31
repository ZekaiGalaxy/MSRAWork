# obj -> stp
# stp -> render
conda activate cad37
python obj2step.py --data_folder example_obj
python render.py  --input_dir example_obj --output_dir example_img