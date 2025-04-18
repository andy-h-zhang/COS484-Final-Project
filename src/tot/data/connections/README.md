---
license: apache-2.0
language:
- en
tags:
- games
- connections
- clustering
pretty_name: New York Times Connections
size_categories:
- 1K<n<10K
---
## Context   
Connections is a word puzzle developed and published by The New York Times, first released on 12 June 2023. It has since become the second most-played game published by the New York Times, behind only Wordle. The player's goal is to identify four distinct categories or themes among sixteen words, with each group containing four words that fit the theme. Words can be connected by various relationships, such as synonyms, shared characteristics, or associations. The connections increase in difficulty (as indicated by the connection's color: yellow (easiest), green, blue, purple (hardest)) as the connections become more abstract or deceptive, with a maximum of four incorrect guesses allowed before the game is over. It tests the player's ability to spot patterns and make associations across different word groupings.

## Content   
This dataset is a collection of NYTimes Connections games and information. Information is displayed by words that appear in each Connections game. Each row contains data on the game ID, date of the game, the word itself, the name of the group it's a part of, the level difficulty of the group, and the original starting position (row and column) of the word.

Refer to the sample NYTimes Connections game below:
![Screenshot of a sample Connections game from 18 August 2023](https://parade.com/.image/t_share/MjAwMTU3OTU2NjMxNzAwODU2/connections-nyt-friday-august-18-2023.png)

You can view the entries for this game in the dataset in indeces 1,072-1,087, or where Game ID is equal to 68. The columns and their properties in the dataset include:
- **Game ID**: The ID of the day's game, as listed by the NYTimes. For the game above, the Game ID is 68.
- **Puzzle Date**: The date of the puzzle, as listed in YYYY-MM-DD. For the game above, the Puzzle Date is 2023-08-18.
- **Word**: Each word from each day's game is listed as a row. Every word is added from the game's starting board, left to right, top to bottom. For example, in the game above, you can find the word 'PINT' in index 1,072, 'REAL' in index 1,073, 'SPONGE' in index 1,076, etc.
- **Group Name**: The theme that connects a word to others in a group. In the game above, the answers are: "Cup, Gallon, Pint, Quart" in yellow (easiest) for "Units of Volume"; "Awful, Quite, Super, Very" in green (moderately easy) for "Extremely"; "Rand, Real, Sterling, Won" in blue (moderately hard) for "World Currencies; and "Carrot, Coffee, Pound, Sponge" in purple (hardest) for "\_\_\_ Cake". So the group names for this game would be 'UNITS OF VOLUME', 'EXTREMELY', 'WORLD CURRENCIES', and '\_\_\_ CAKE'.
- **Group Level**:  The difficulty of the group, indicated by an integer (0 being easiest, 3 being the hardest). As an example, in the game above, "World Currencies" is grouped in blue (second hardest, third easiest), meaning its group level would be 2.
- **Starting Row**: The starting row position for a given word, expressed as an integer 1-4. Rows are numbered from top to bottom, so 1 is the topmost row, while 4 is the bottommost row.
- **Starting Column**: The starting column position for a given word, expressed as an integer 1-4. Columns are numbered from left to right, so 1 is the leftmost row, while 4 is the rightmost row.

To put the starting rows and columns together, here is a visual example of the starting rows & columns for the game above, expressed as "WORD: (row, column)":

| PINT: (1, 1) | REAL: (1, 2) | CARROT: (1, 3) | AWFUL: (1, 4) |
| --- | --- | --- | --- |
| SPONGE: (2, 1) | CUP: (2, 2) | WON: (2, 3) | SUPER: (2, 4) |
| GALLON: (3, 1) | COFFEE: (3, 2) | VERY: (3, 3) | POUND: (3, 4) |
| RAND: (4, 1) | QUITE: (4, 2) | QUART: (4, 3) | STERLING: (4, 4) |


## Acknowledgements   
All game information was collected from the NYTimes archive.

## Inspiration   
Some possible uses for this dataset include:
- Evaluating Reasoning and Decision Making skills of LLMs/Neural Networks ([recent paper on this topic](https://arxiv.org/abs/2406.11012))
- Using NLP analysis to detect "red herrings" in Connections
- Utilizing the work to construct a word association network