# sorting_battle_gym package
## GameState class
### var
```python
dict config {
    'player_count': int # 1 or 2
}
```
### Public Method
> These are public methods to call from outisde (the RL model)
- GameState(dict config)
    - The constructor of the gym
- set_callback(callback cb, int player_id=1) 
    - sets the callback function to be called when the player can take action
- void run_game()
    - a blocking function that runs the game until it ends.
    - the gym will call agent_callback() when agent can take action
```python
# the callback function should have the following interface
def agent_callback(game_end, level, grid1, score1, gird2=None, score2=None):
    '''
    :param game_end: int, (for 1P) 0 for not end, 1 for lose
                     int, (for 2P) 0 for not end, 1 for player 1 wins, 2 for player 2 wins
    :param level: int, current level of game

    :param grid1: 2D-list of int, current grid of the player where -1 is empty, -2 is garbage, other valid values are >= 0
    :param score1: int, current score of the player

    (for 2P, the following 3 parameters will not be passed in 1P mode)
    :param grid2: 2D-list of int, current grid of the opponent where -1 is empty, -2 is garbage, other valid values are >= 0
    :param score2: int, current score of the opponent
    
    :return action_type, coord_list: 
        action_type: int, 0 for idle, 1 for swap, 2 for select
        coord_list: list of tuple, 
                    for swap: [(row1, column1), (row2, column2)]
                    for select: [(row, column), ...]
    '''
    # do stuff
    return action_type, coord_list
```
### Usage
> The following is an example of how to use the gym in 1P mode
```python
from sorting_battle_gym.game_state import GameState

# define the callback function
def player1_callback(game_end, level, grid1, score1, gird2=None, score2=None):
    # make a decision for player 1
    return action_type, coord_list

# initialize the gym
config = {
    'player_count': 1
}
game_state = GameState(config)
# set the callback function
game_state.set_callback(player1_callback, 1)
# run the game
game_state.run_game()
```