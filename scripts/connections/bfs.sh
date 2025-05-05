python run.py \
    --backend gpt-4 \
    --task connections \
    --task_start_index 101 \
    --task_end_index 105 \
    --method_generate propose \
    --method_evaluate value \
    --method_select greedy \
    --n_evaluate_sample 3 \
    --n_select_sample 5 \
    ${@}
