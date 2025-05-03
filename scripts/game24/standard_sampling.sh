python run.py \
    --backend gpt-4o-mini \
    --task game24 \
    --task_start_index 800 \
    --task_end_index 810 \
    --naive_run \
    --prompt_sample standard \
    --n_generate_sample 100 \
    ${@}