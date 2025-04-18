python run.py \
    --backend gpt-4o \
    --task game24 \
    --task_start_index 800 \
    --task_end_index 801 \
    --naive_run \
    --prompt_sample cot \
    --n_generate_sample 1 \
    ${@}