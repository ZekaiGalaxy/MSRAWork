#!/bin/bash
input_base_dir="../../MSRAWork/CADTool/test"
output_base_dir="../../test_pictures"

for dir in "$input_base_dir"*; do
    if [ -d "$dir" ]; then
        folder_name=$(basename "$dir")
        output_dir="$output_base_dir/$folder_name/imgs"
        echo $dir
        python cad_img.py --input_dir "$dir" --output_dir "$output_dir"
    fi
done