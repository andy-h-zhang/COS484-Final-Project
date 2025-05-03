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
    
    # --------------------------------------------------------------------
    # POST‑PROCESS: add clean Answer‑lines so tester passes
    # --------------------------------------------------------------------
    if args.task == 'game24':
        solved_pattern = re.compile(r'.*= *24 *(?:\([^)]*24\))? *$', re.I)

        ys = [add_answer_line(y) if solved_pattern.search(y.split('\n')[-1])
            else y
            for y in ys]

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
import sympy


# --------------------------------------------------------------------------
# helper: build a single parenthesised expression from the chain of moves
# --------------------------------------------------------------------------
def build_expression(chain: str) -> str:
    """
    Convert every line '<exprA> op <exprB> = <val> …' into nested parentheses.
    Anything after the first '(' (the 'left: …' tag) is ignored.
    """
    value2expr = {}
    # allow optional leading bullet / number and ignore trailing junk
    pat = re.compile(r'''
        ^\s*           # optional leading spaces
        (?:\d+\.\s*)?  # optional "12. "
        ([^(=]+?)      # exprA  (no '(' or '=' yet)
        \s*([+\-*/])\s*
        ([^(=]+?)      # exprB
        \s*=\s*
        ([0-9.\-]+)    # result value
        ''', re.X)

    for ln in chain.strip().split('\n'):
        ln_core = ln.split('(')[0]          # drop " (left: …"
        m = pat.match(ln_core)
        if not m:
            continue
        a_raw, op, b_raw, res = (t.strip() for t in m.groups())
        # resolve operands if they were produced earlier
        a = value2expr.get(a_raw, a_raw)
        b = value2expr.get(b_raw, b_raw)
        value2expr[res] = f"({a} {op} {b})"

    return value2expr.get('24', '24')


def add_answer_line(chain: str) -> str:
    expr = build_expression(chain)
    try:
        if sympy.simplify(expr) != 24:
            return chain                     # skip if we failed to build
    except Exception:
        print("could not build answer")
        return chain
    return chain.rstrip() + f"\nAnswer: {expr} = 24\n"

# --------------------------------------------------------------------------
def astar_solve(args, task, idx, to_print=True):
    import heapq, re, sympy, itertools
    from functools import partial

    # ---- helpers --------------------------------------------------------
    def canonical(chain: str) -> str:
        "strip trailing/leading blanks and collapse repeated whitespace"
        import re
        lines = [re.sub(r'\s+', ' ', ln).strip() for ln in chain.split('\n') if ln.strip()]
        return '\n'.join(lines)

    # build_expression & add_answer_line come from your earlier snippet
    # --------------------------------------------------------------------
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    x = task.get_input(idx)

    cost      = lambda y: -get_value(task, x, y, args.n_evaluate_sample)
    heuristic = lambda y: 0

    beam = args.n_select_sample                # keep at most this many nodes
    open_list = [(0, 0, '')]                   # (f,g,chain)
    finished, finished_set = [], set()         # avoid dup solutions
    infos, step = [], 0
    max_depth = max(task.steps, 5)

    goal_regex = re.compile(r'.*= *24 *(?:\([^)]*24\))? *$', re.I)

    while open_list and len(finished) < beam:
        f_curr, g_curr, y_curr = heapq.heappop(open_list)

        # -------- goal test ---------------------------------------------
        if y_curr and goal_regex.search(y_curr.split('\n')[-1]):
            y_norm = canonical(y_curr)
            if y_norm not in finished_set:         # skip exact dup
                y_curr = add_answer_line(y_curr)
                finished.append(y_curr)
                finished_set.add(y_norm)
                if to_print:
                    print(f"Solution {len(finished)}/{beam}:\n{y_curr}\n")
            continue

        # -------- depth cap ---------------------------------------------
        if y_curr and len(y_curr.split('\n')) >= max_depth:
            continue

        # -------------------------------- children ------------------------------
        children = [c for c in get_proposals(task, x, y_curr) if c.strip()]
        values   = [get_value(task, x, c, args.n_evaluate_sample) for c in children]

        # rank all children by value
        ranked   = sorted(range(len(children)), key=lambda i: values[i], reverse=True)

        kept_ids = []                       # after duplicate filtering
        for i in ranked:
            c_key = canonical(children[i])
            if c_key in finished_set:       # already solved → skip
                continue
            kept_ids.append(i)
            if len(kept_ids) == beam:       # got enough new nodes
                break

        # -------- fallback: if nothing left, keep the single best anyway ---------
        if not kept_ids and children:
            kept_ids = ranked[:1]           # push the highest‑value duplicate

        # ------------------------------------------------------------------------
        for i in kept_ids:
            c = children[i]
            g_new = g_curr + cost(c)
            f_new = g_new + heuristic(c)
            heapq.heappush(open_list, (f_new, g_new, c))
            
        # ---- global beam prune (controls heap size) --------------------
        open_list[:] = heapq.nsmallest(beam, open_list)
        heapq.heapify(open_list)

        # ---- logging ---------------------------------------------------
        infos.append({
            'step': step,
            'x': x,
            'ys': [y_curr],
            'new_ys': children,
            'values': values,
            'select_new_ys': [children[i] for i in best_ids],
        })
        if to_print:
            print(f"Step {step}: expanded depth={len(y_curr.splitlines())}")
            print("  *** reached detail block ***")
            print(f"ys:  {[y_curr]}")
            print(f"new_ys:  {children}")
            print(f"values: {values}")
            print(f"select_new_ys: {[children[i] for i in best_ids]}")
        step += 1

    if to_print:
        print("\nFinal solutions:")
        for sol in finished:
            print(sol)

    return finished, {'steps': infos}