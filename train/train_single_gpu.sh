python train.py \
    --model_name_or_path "/f_ndata/zekai/models/CodeLlama-7b-hf" \
    --data_path "/f_ndata/zekai/data/cad_data.txt" \
    --output_dir "/f_ndata/zekai/trained_cad" \
    --num_train_epochs 10 \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 8 \
    --gradient_accumulation_steps 1 \
    --evaluation_strategy "no" \
    --save_strategy "epoch" \
    --save_steps 100 \
    --save_total_limit 5 \
    --learning_rate 3e-5 \
    --warmup_steps 100 \
    --logging_steps 1 \
    --dataloader_num_workers 20 \
    --lr_scheduler_type "cosine" \
    --report_to "tensorboard" \
    --gradient_checkpointing True \
    --fp16 True \
    --remove_unused_columns False