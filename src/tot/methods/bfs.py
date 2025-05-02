import itertools
import numpy as np
from functools import partial
from tot.models import gpt

# for astar
import heapq


def get_value(task, x, y, n_evaluate_sample, cache_value=True):
    value_prompt = task.value_prompt_wrap(x, y)
    if cache_value and value_prompt in task.value_cache:
        return task.value_cache[value_prompt]
    value_outputs = gpt(value_prompt, n=n_evaluate_sample, stop=None)
    value = task.value_outputs_unwrap(x, y, value_outputs)
    if cache_value:
        task.value_cache[value_prompt] = value
    return value

def get_values(task, x, ys, n_evaluate_sample, cache_value=True):
    values = []
    local_value_cache = {}
    for y in ys:  # each partial output
        if y in local_value_cache:  # avoid duplicate candidates
            value = 0
        else:    
            value = get_value(task, x, y, n_evaluate_sample, cache_value=cache_value)
            local_value_cache[y] = value
        values.append(value)
    return values

def get_votes(task, x, ys, n_evaluate_sample):
    vote_prompt = task.vote_prompt_wrap(x, ys)
    vote_outputs = gpt(vote_prompt, n=n_evaluate_sample, stop=None)
    values = task.vote_outputs_unwrap(vote_outputs, len(ys))
    return values

def get_proposals(task, x, y): 
    propose_prompt = task.propose_prompt_wrap(x, y)
    proposals = gpt(propose_prompt, n=1, stop=None)[0].split('\n')
    return [y + _ + '\n' for _ in proposals]

def get_samples(task, x, y, n_generate_sample, prompt_sample, stop):
    if prompt_sample == 'standard':
        prompt = task.standard_prompt_wrap(x, y)
    elif prompt_sample == 'cot':
        prompt = task.cot_prompt_wrap(x, y)
    else:
        raise ValueError(f'prompt_sample {prompt_sample} not recognized')
    samples = gpt(prompt, n=n_generate_sample, stop=stop)
    return [y + _ for _ in samples]

def solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    print(gpt)
    x = task.get_input(idx)  # input
    ys = ['']  # current output candidates
    infos = []
    for step in range(task.steps):
        # generation
        if args.method_generate == 'sample':
            new_ys = [get_samples(task, x, y, args.n_generate_sample, prompt_sample=args.prompt_sample, stop=task.stops[step]) for y in ys]
        elif args.method_generate == 'propose':
            new_ys = [get_proposals(task, x, y) for y in ys]
        new_ys = list(itertools.chain(*new_ys))
        ids = list(range(len(new_ys)))
        # evaluation
        if args.method_evaluate == 'vote':
            values = get_votes(task, x, new_ys, args.n_evaluate_sample)
        elif args.method_evaluate == 'value':
            values = get_values(task, x, new_ys, args.n_evaluate_sample)

        # selection
        if args.method_select == 'sample':
            ps = np.array(values) / sum(values)
            select_ids = np.random.choice(ids, size=args.n_select_sample, p=ps).tolist()
        elif args.method_select == 'greedy':
            select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:args.n_select_sample]
        select_new_ys = [new_ys[select_id] for select_id in select_ids]

        # log
        if to_print: 
            sorted_new_ys, sorted_values = zip(*sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True))
            print(f'-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n')
        
        infos.append({'step': step, 'x': x, 'ys': ys, 'new_ys': new_ys, 'values': values, 'select_new_ys': select_new_ys})
        ys = select_new_ys
    
    if to_print: 
        print(ys)
    return ys, {'steps': infos}

def naive_solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    print(gpt)
    x = task.get_input(idx)  # input
    ys = get_samples(task, x, '', args.n_generate_sample, args.prompt_sample, stop=None)
    return ys, {}

import heapq
import re
from functools import partial


def is_finished(chain: str) -> bool:
    """Return True if the last line has no 'left:' (i.e., answer found)."""
    last = chain.strip().split('\n')[-1]
    return 'left:' not in last


def astar_solve(args, task, idx, to_print=True):
    def strip_blank_lines(lines):
        return [ln for ln in (l.strip() for l in lines) if ln]


    def is_finished(chain: str) -> bool:
        """Finished when the last non‑blank line has *no* 'left:' field."""
        last = strip_blank_lines(chain.split('\n'))[-1]
        return 'left:' not in last.lower()


    def num_moves(chain: str) -> int:
        """Count the non‑blank lines in the chain (root has 0 moves)."""
        return len(strip_blank_lines(chain.split('\n')))
    
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)

    x = task.get_input(idx)

    # cost = −reward ; heuristic left as 0
    cost = lambda y: -get_value(task, x, y, args.n_evaluate_sample)
    heuristic = lambda y: 0

    open_list = []                                   # (f, g, chain)
    heapq.heappush(open_list, (0, 0, ''))            # root
    closed = set()

    finished = []                                    # completed solutions
    infos = []
    step = 0
    max_depth = max(task.steps, 5)                   # root + up‑to‑4 moves

    while open_list and len(finished) < args.n_select_sample:

        f_curr, g_curr, y_curr = heapq.heappop(open_list)
        if y_curr in closed:
            continue
        closed.add(y_curr)

        # ---------------- goal test ----------------------------------------
        if num_moves(y_curr) > 0 and is_finished(y_curr):
            finished.append(y_curr)
            if to_print:
                print(f"Solution {len(finished)}/{args.n_select_sample}\n{y_curr}\n")
            continue

        if num_moves(y_curr) >= max_depth:           # depth cap
            continue

        # ---------------- generation ---------------------------------------
        raw_children = get_proposals(task, x, y_curr)            # model call
        children = [ln + '\n' for ln in strip_blank_lines(raw_children)]

        # ---------------- evaluation ---------------------------------------
        values = [get_value(task, x, c, args.n_evaluate_sample) for c in children]

        # select top‑k children
        ids = sorted(range(len(children)), key=lambda i: values[i], reverse=True)
        kept_ids = ids[:args.n_select_sample]
        kept_children = []

        for i in kept_ids:
            c = children[i]
            kept_children.append(c)

            if is_finished(c):
                finished.append(c)
                if len(finished) == args.n_select_sample:
                    break
                continue

            g_child = g_curr + cost(c)
            f_child = g_child + heuristic(c)
            heapq.heappush(open_list, (f_child, g_child, c))

        # global beam prune
        open_list[:] = heapq.nsmallest(args.n_select_sample, open_list)
        heapq.heapify(open_list)

        # ---------------- logging ------------------------------------------
        infos.append({
            'step': step,
            'x': x,
            'ys': [y_curr],            # like BFS: survivors entering this step
            'new_ys': children,
            'values': values,
            'select_new_ys': kept_children,
        })

        if to_print:
            print(f"Step {step}: expanded depth={num_moves(y_curr)}")
            print("  kept:", kept_children, "\n")

        step += 1

    if to_print:
        print("Final solutions:")
        for sol in finished:
            print(sol)

    return finished, {'steps': infos}
