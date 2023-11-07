deepspeed --num_gpus 8 \
    --num_nodes 1 \
    train.py \
    --model_name_or_path "/f_ndata/zekai/models/CodeLlama-7b-hf" \
    --data_path "/f_ndata/zekai/data/cad_data.txt" \
    --output_dir "/f_ndata/zekai/trained_cad" \
    --num_train_epochs 5 \
    --per_device_train_batch_size 64 \
    --per_device_eval_batch_size 64 \
    --gradient_accumulation_steps 1 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 100 \
    --learning_rate 3e-5 \
    --warmup_steps 20 \
    --logging_steps 1 \
    --lr_scheduler_type "cosine" \
    --report_to "tensorboard" \
    --gradient_checkpointing True \
    --deepspeed ds_config1.json \
    --fp16 True \
    --remove_unused_columns False
    # --fp16 True \