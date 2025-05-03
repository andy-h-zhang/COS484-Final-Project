python run.py \
    --backend gpt-4o-mini \
    --task connections \
    --task_start_index 100 \
    --task_end_index 101 \
    --method_generate propose \
    --method_evaluate value \
    --method_select greedy \
    --n_evaluate_sample 3 \
    --n_select_sample 5 \
    ${@}
