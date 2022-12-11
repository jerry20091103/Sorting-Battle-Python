# sorting_battle_gym package
> NOTE: There is now a interactive terminal version of the game. You can play it by running `python 1p_terminal_game.py` in the **game folder**. 
## GameBase class
### var
```python
dict config {
    'player_count': int # 1 or 2
    'player_swap_delay': int # simulated delay for AI in ticks
    'player_select_delay': int # simulated delay for AI in ticks
    'realtime': bool # whether to run the game in realtime
    # Each tick is 1/50 second (0.02 second)
}
```
### Public Method
> These are public methods to call from outisde (the RL model)
- GameBase(dict config)
    - The constructor of the gym
- set_callback(callback cb, int player_id=1) 
    - sets the callback function to be called when the player can take action
- void run_game()
    - a blocking function that runs the game until it ends.
    - the gym will call agent_callback() when agent can take action
- The callback function is as follows:
```python
# the callback function should have the following interface
# This functions is called when it's time for the agent to take action
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
                    for idle: []
                    for swap: [(row1, column1), (row2, column2)]
                    for select: [(row, column), ...]
    '''
    # do stuff
    return action_type, coord_list
```
### Usage
> The following is an example of how to use the gym in 1P mode
```python
from sorting_battle_gym.game_base import GameBase

# initialze the ML model (we use "model" as an example
model_player1 = Model(...)

# define the callback function
def player1_callback(game_end, level, grid1, score1, gird2=None, score2=None):
    # the model gets the current state of the game
    current_state = (level, grid1, score1)
    # and uses the replay memory as well as the current state to learn
    model_player1.learn(current_state)
    # the model takes action according to current state of the game
    action = model_player1.take_action(current_state)
    # the current state is stored to replay memory for future learning
    model_player1.store_state(current_state)
    # convert the action to the format that the gym can understand
    action_type, coord_list = action...
    # give the action to the gym
    return action_type, coord_list

# initialize the gym
config = {
    'player_count': 1,
    'player_swap_delay': 10,
    'player_select_delay': 50,
    'realtime': False
}
game_base = GameBase(config)
# set the callback function
game_base.set_callback(player1_callback, 1)
# run the game
game_base.run_game()
```
> The following is an example of how to use the gym in 2P mode
- The 2P mode is very similar to the 1P mode, except that there are two instance of the model and two callback functions
```python
from sorting_battle_gym.game_base import GameState

# initialze 2 ML models (we use "Model" as an example
model_player1 = Model(...)
model_player2 = Model(...)

# define the callback function for player 1
def player1_callback(game_end, level, grid1, score1, gird2=None, score2=None):
    # the model gets the current state of the game
    # In 2P mode you also get the opponent's (player 2's) grid and score
    current_state = (level, grid1, score1, grid2, score2)
    # and uses the replay memory as well as the current state to learn
    model_player1.learn(current_state)
    # the model takes action according to current state of the game
    action = model_player1.take_action(current_state)
    # the current state is stored to replay memory for future learning
    model_player1.store_state(current_state)
    # convert the action to the format that the gym can understand
    action_type, coord_list = action...
    # give the action to the gym
    return action_type, coord_list

# define the callback function for player 2
def player2_callback(game_end, level, grid1, score1, gird2=None, score2=None):
    # the model gets the current state of the game
    # In 2P mode you also get the opponent's (player 1's) grid and score
    current_state = (level, grid1, socre1, grid2, score2)
    # and uses the replay memory as well as the current state to learn
    model_player2.learn(current_state)
    # the model takes according to current state of the game
    action = model_player2.take_action(current_state)
    # the current state is stored to replay memory for future learning
    model_player2.store_state(current_state)
    # convert the action to the format that the gym can understand
    action_type, coord_list = action...
    # give the action to the gym
    return action_type, coord_list

# initialize the gym
config = {
    'player_count': 2
    'player_swap_delay': 10,
    'player_select_delay': 50,
    'realtime': False
}
game_base = GameState(config)
# set the callback function for player 1 and player 2
game_base.set_callback(player1_callback, 1)
game_base.set_callback(player2_callback, 2)
# run the game
game_base.run_game()
```