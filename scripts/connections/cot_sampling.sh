python run.py \
    --backend gpt-4o-mini \
    --task connections \
    --task_start_index 100 \
    --task_end_index 101 \
    --naive_run \
    --prompt_sample cot \
    --n_generate_sample 10 \
    ${@}