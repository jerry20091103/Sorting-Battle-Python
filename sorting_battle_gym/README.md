# sorting_battle_gym package
> NOTE: There is now a interactive terminal version of the game. You can play it by running `python 1p_terminal_game.py` in the **game folder**. 
## GameBase class
### variables
- config: dict for GameBase constructor:
```python
dict config {
    'player_count': int # 1 or 2
    'player_swap_delay': int # simulated delay for AI in ticks
    'player_select_delay': int # simulated delay for AI in ticks
    'realtime': bool # whether to run the game in realtime
    # Each tick is 1/50 second (0.02 second)
}
```
- game_status: dict passed to the agent callback function in **1P mode**:
```python
dict game_status {
    'game_end': int # 0 for not end, 1 for lose
    'level': int # current level of game
    'grid': 2D-list of int # current grid of the player 
                           # where -1 is empty, -2 is garbage, other valid values are >= 0
    'score': int # current score of the player
}
```
- game_status_2p: dict passed to the agent callback function in **2P mode**:
```python
dict game_status_2p {
    'game_end': int # 0 for not end, 1 for lose
    'level': int # current level of game
    'grid': 2D-list of int # current grid of the player 
                           # where -1 is empty, -2 is garbage, other valid values are >= 0
    'score': int # current score of the player
    'opponent_grid': 2D-list of int # current grid of the opponent
                                    # where -1 is empty, -2 is garbage, other valid values are >= 0
    'opponent_score': int # current score of the opponent
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
def agent_callback(game_status):
    '''
    :param game_status: dict, the current status of the game (see above)
    
    :return action_type, action_data: 
        action_type: int, 0 for idle, 1 for swap, 2 for select
        action_data: for idle: int, number of ticks to idle
                     for swap: list of 2 tuples, [(row1, column1), (row2, column2)]
                     for select: list of tuples,  [(row, column), ...]
    '''
    # do stuff
    return action_type, action_data
```
### Usage
> The following is an example of how to use the gym in 1P mode
```python
from sorting_battle_gym.game_base import GameBase

# initialze the ML model (we use "model" as an example
model_player1 = Model(...)

# define the callback function
def player1_callback(game_state):
    # the model gets the current state of the game
    current_state = game_state...
    # and uses the replay memory as well as the current state to learn
    model_player1.learn(current_state)
    # the model takes action according to current state of the game
    action = model_player1.take_action(current_state)
    # the current state is stored to replay memory for future learning
    model_player1.store_state(current_state)
    # convert the action to the format that the gym can understand
    action_type, action_data = action...
    # give the action to the gym
    return action_type, action_data

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
def player1_callback(game_state_2p):
    # the model gets the current state of the game
    current_state = game_state_2p...
    # and uses the replay memory as well as the current state to learn
    model_player1.learn(current_state)
    # the model takes action according to current state of the game
    action = model_player1.take_action(current_state)
    # the current state is stored to replay memory for future learning
    model_player1.store_state(current_state)
    # convert the action to the format that the gym can understand
    action_type, action_data = action...
    # give the action to the gym
    return action_type, action_data

# define the callback function for player 2
def player2_callback(game_state_2p):
    # the model gets the current state of the game
    current_state = game_state_2p...
    # and uses the replay memory as well as the current state to learn
    model_player2.learn(current_state)
    # the model takes according to current state of the game
    action = model_player2.take_action(current_state)
    # the current state is stored to replay memory for future learning
    model_player2.store_state(current_state)
    # convert the action to the format that the gym can understand
    action_type, action_data = action...
    # give the action to the gym
    return action_type, action_data

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