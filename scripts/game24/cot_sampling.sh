python run.py \
    --backend gpt-4 \
    --task game24 \
    --task_start_index 800 \
    --task_end_index 805 \
    --naive_run \
    --prompt_sample cot \
    --n_generate_sample 10 \
    ${@}