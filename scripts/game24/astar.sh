python run.py \
    --backend gpt-4o-mini \
    --task game24 \
    --task_start_index 800 \
    --task_end_index 801 \
    --astar_run \
    --method_generate propose \
    --method_evaluate value \
    --method_select greedy \
    --n_evaluate_sample 3 \
    --n_select_sample 5 \
    ${@}
