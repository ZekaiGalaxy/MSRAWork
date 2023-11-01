# obj -> stp
# stp -> render
conda activate cad37
python obj2code.py
python obj2step.py --data_folder example_obj
python render.py  --input_dir example_obj --output_dir example_img
python obj2step.py --data_folder formatted_obj
python render.py  --input_dir formatted_obj --output_dir formatted_img



# sometimes rounding can lead to same point location!
# We should discard these data!