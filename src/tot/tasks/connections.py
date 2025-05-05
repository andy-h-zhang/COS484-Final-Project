import re
import os
import sympy
import random
import pandas as pd
from tot.tasks.base import Task, DATA_PATH
from tot.prompts.connections import * 

# To Do:
# (1) Make connections prompts
# (2) Update __init__.py to reflect the addition of Connections

def get_current_guess(y: str) -> str:
    # last_line = y.strip().split('\n')[-1]
    # return last_line.split('left: ')[-1].split(')')[0]
    last_line = y.strip().split('\n')[-1]
    if 'left: ' in last_line:
        return last_line.split('left: ')[-1].split(')')[0].strip()
    # new: if this is still the original input, we haven’t formed a group yet
    return ''

    
    ## Code that works for Standard/COT
    # last_line = y.strip().split('\n')[-1]
    # return last_line.split('Output: ')[-1]

class ConnectionsTask(Task):
    """
    Input (x)   : a string of 16 words
    Output (y)  : a trajectory of 4 groups to complete the Connections groups
    Reward (r)  : 0, 1, 2, 3, or 4, depending on how many groups are correct
    """
    def __init__(self, file='Connections_Data.csv'):
        """
        file: a csv file (fixed)
        """
        super().__init__()
        self.steps = 4
        self.value_cache = {}
        path = os.path.join(DATA_PATH, 'connections', file)
        # debug path
        print(f"Loading CSV from: {path}")
        df = pd.read_csv(path)
        # puzzles with 4 unique groups and 16 total words
        self.puzzles = {
            game_id: group_df for game_id, group_df in df.groupby('Game ID')
            if group_df['Group Name'].nunique() == 4 and len(group_df) == 16
        }
        self.game_ids = list(self.puzzles.keys())

    def __len__(self) -> int:
        return len(self.puzzles)
    
    def get_input(self, idx: int) -> str:
        words = list(self.puzzles[self.game_ids[idx]]['Word'])
        return ' '.join(words)

    def test_output(self, idx: int, output: str):
        # # For COT/Standard
        # # correct groupings
        # correct_df = list(self.puzzles.values())[idx]
        # correct_groupings = correct_df.groupby('Group Name')['Word'].apply(lambda x: sorted(x.tolist())).tolist()

        # # dissect LLM output
        # last_line = output.strip().split('\n')[-1]
        # if 'Output:' in last_line:
        #     last_line = last_line.split('Output:')[-1].strip()

        # guessed_groups = [sorted(group.strip().split()) for group in last_line.split(',')]

        # # confirm output is correct format
        # if len(guessed_groups) != 4 or any(len(group) != 4 for group in guessed_groups):
        #     return {'r': 0}

        # # sort lists
        # guessed_groups_sorted = sorted(guessed_groups)
        # correct_groupings_sorted = sorted(correct_groupings)

        # # return answer
        # correct_set = [set(g) for g in correct_groupings]
        # guess_set = [set(g) for g in guessed_groups]

        # num_correct = sum(1 for g in guess_set if g in correct_set)
        # return {'r': num_correct}

        ## For TOT
        # 1) load correct answers
        correct_df = list(self.puzzles.values())[idx]
        correct_group_sets = [
            set(words) for words in
            correct_df.groupby('Group Name')['Word']
                    .apply(list)
        ]

        # 2) split into non‐empty lines and take first 4
        lines = [line.strip() for line in output.strip().split('\n') if line.strip()]
        lines = lines[:4]

        # 3) parse each line --> first 4 tokens before any '('
        guessed_sets = []
        for line in lines:
            # drop any leading "Output:" if present
            if line.startswith('Output:'):
                line = line[len('Output:'):].strip()
            # keep only the text before the first "("
            content = line.split('(')[0].strip()
            tokens = content.split()
            if len(tokens) < 4:
                # malformed line
                return {'r': 0}
            guessed_sets.append(set(tokens[:4]))

        # 5) count how many guessed sets match any correct set
        num_correct = sum(1 for g in guessed_sets if g in correct_group_sets)
        return {'r': num_correct}


        ## remove this one
        # # 4) must have exactly 4 groups of size 4 
        # if len(guessed_sets) != 4 or any(len(g)!=4 for g in guessed_sets):
        #     return {'r': 0}

    @staticmethod
    def standard_prompt_wrap(x: str, y:str='') -> str:
        return standard_prompt.format(input=x) + y

    @staticmethod
    def cot_prompt_wrap(x: str, y:str='') -> str:
        return cot_prompt.format(input=x) + y
    
    @staticmethod
    def propose_prompt_wrap(x: str, y: str='') -> str:
        ## Proper valuing, but no iteration
        # current_guess = get_current_guess(y if y else x)
        # if current_guess == '':
        #     return cot_prompt.format(input=x) + '\nThoughts:' + (y if y else '')
        # # otherwise keep proposing next groups
        # return propose_prompt.format(input=current_guess)

        # 1) no history yet --> brainstorm first group
        if not y.strip():
            return propose_prompt.format(input=x)
        # 2) we have some groups in y --> extract leftover and propose next
        leftover = get_current_guess(y)
        if leftover:
            return propose_prompt.format(input=leftover)
        # 3) no leftovers --> switch to COT/finalization
        return cot_prompt.format(input=x) + '\nThoughts:' + y
        
        # if len(current_guess.split()) == 4:
        #     prompt = cot_prompt.format(input=x) + 'Thoughts:' + y
        #     # print([prompt])
        # else:
        #     prompt = propose_prompt.format(input=current_guess)
        # return prompt

        # last_line = y.strip().split('\n')[-1] if y.strip() else ''
        # if last_line.lower().startswith('output:'):
        #     return ''
        # return propose_prompt.format(input=x)
    
    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        last_line = y.strip().split('\n')[-1]
        if 'left: ' not in last_line:
            # strip the cue and pass only the groups to the rubric prompt
            ans = last_line.split('Output:')[-1].strip()
            # print([value_last_step_prompt.format(input=x, answer=ans)])
            return value_last_step_prompt.format(input=x, output=ans)
        current_guess = get_current_guess(y)
        return value_prompt.format(input=current_guess)
    
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        # # if already four Thoughts + Output --> close out early
        # if len(y.strip().split('\n')) == 4 and 'output:' in y.lower():
        #     return 1.0

        # nums = []
        # for out in value_outputs:
        #     last = out.strip().split('\n')[-1]
        #     m = re.search(r'([01](?:\.\d+)?)', last)
        #     if m:
        #         nums.append(float(m.group(1)))
        # return sum(nums)/len(nums) if nums else 0.0
        
        if len(y.strip().split('\n')) == 4 and 'value' not in y.lower():
            return 0
        scores = []
        for output in value_outputs:
            last_line = output.strip().split('\n')[-1].strip().lower()
            try:
                val = float(last_line)
                if 0.0 <= val <= 1.0:
                    scores.append(val)
            except ValueError:
                continue
        return sum(scores) / len(scores) if scores else 0.0
        
        
        # value_names = [_.split('\n')[-1] for _ in value_outputs]
        # value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        # value = sum(value * value_names.count(name) for name, value in value_map.items())
        # return value
    
# # test
# if __name__ == "__main__":
#     task = ConnectionsTask()

#     print(f"Loaded {len(task)} puzzles.")

#     idx = 20
#     x = task.get_input(idx)
#     print(f"Puzzle Input (16 words):\n{x}")

#     correct_df = list(task.puzzles.values())[idx]
#     grouped = correct_df.groupby('Group Name')['Word'].apply(lambda x: sorted(x.tolist())).tolist()
#     fake_output = 'Output: ' + ', '.join([' '.join(group) for group in grouped])

#     print(f"\nFake Output:\n{fake_output}")
#     result = task.test_output(idx, fake_output)
#     print(f"\nResult of test_output: {result}")
