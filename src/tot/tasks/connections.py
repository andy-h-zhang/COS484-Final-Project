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
    last_line = y.strip().split('\n')[-1]
    return last_line.split('left: ')[-1].split(')')[0]

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
        path = os.path.join(DATA_PATH, 'Connections_Data', file)
        df = pd.read_csv(path)
        self.puzzles = {
            game_id: group_df for game_id, group_df in df.groupby('Game ID')
            if group_df['Group Name'].nunique() == 4 and len(group_df) == 16
        }
        self.game_ids = list(self.puzzles.keys())
        self.current_game_id = random.choice(self.game_ids)
        self.current_puzzle_df = self.puzzles[self.current_game_id]

        self.words = list(self.current_puzzle_df['Word'])
        self.remaining_words = set(self.words)
        self.groupings = self.current_puzzle_df[['Word', 'Group Name']].set_index('Word').to_dict()['Group Name']
        self.correct_groups = set()
        self.attempts_left = 4

    def __len__(self) -> int:
        return len(self.puzzles)
    
    def get_input(self, idx: int) -> str:
        return self.puzzles[idx]

    def test_output(self, idx: int, output: str):
        # correct groupings
        correct_df = list(self.puzzles.values())[idx]
        correct_groupings = correct_df.groupby('Group Name')['Word'].apply(lambda x: sorted(x.tolist())).tolist()

        # dissect LLM output
        last_line = output.strip().split('\n')[-1]
        if 'Output:' in last_line:
            last_line = last_line.split('Output:')[-1].strip()

        guessed_groups = [sorted(group.strip().split()) for group in last_line.split(',')]

        # confirm output is correct format
        if len(guessed_groups) != 4 or any(len(group) != 4 for group in guessed_groups):
            return {'r': 0}

        # sort lists
        guessed_groups_sorted = sorted(guessed_groups)
        correct_groupings_sorted = sorted(correct_groupings)

        # return answer
        if guessed_groups_sorted == correct_groupings_sorted:
            return {'r': 1}
        else:
            return {'r': 0}

    @staticmethod
    def standard_prompt_wrap(x: str, y:str='') -> str:
        return standard_prompt.format(input=x) + y

    @staticmethod
    def cot_prompt_wrap(x: str, y:str='') -> str:
        return cot_prompt.format(input=x) + y
    
    @staticmethod
    def propose_prompt_wrap(x: str, y: str='') -> str:
        current_numbers = get_current_numbers(y if y else x)
        if current_numbers == '24':
            prompt = cot_prompt.format(input=x) + 'Steps:' + y
            # print([prompt])
        else:
            prompt = propose_prompt.format(input=current_numbers)
        return prompt
    
    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        last_line = y.strip().split('\n')[-1]
        if 'left: ' not in last_line:  # last step
            ans = last_line.lower().replace('answer: ', '')
            # print([value_last_step_prompt.format(input=x, answer=ans)])
            return value_last_step_prompt.format(input=x, answer=ans)
        current_numbers = get_current_numbers(y)
        return value_prompt.format(input=current_numbers)
    
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        if len(y.strip().split('\n')) == 4 and 'answer' not in y.lower():
            return 0
        value_names = [_.split('\n')[-1] for _ in value_outputs]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        return value