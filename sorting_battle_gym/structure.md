# Sorting Battle Code Structure
## GameBase
### var
- dict config {
    - int player_count
    - int player_swap_delay 
    - int player_select_delay
    - bool realtime
}
- int player_count
- bool realtime
- GameState game_state
### method
- GameBase(dict config)
    - initialize the game and the constructor of required game modes
- void run_game()
    - call the run_game() of the game mode
- void set_callback(callback cb, int player_id=1)
    - call the set_player_callback() of the game mode
## GameState (ABC)
### var
- int current_tick
- queue.PriorityQueue task_queue
- int player_swap_delay 
- int player_select_delay
- int level
- bool game_over
### method
- GameState(player_swap_delay, player_select_delay) **(abstract)**
- void run_game(bool realtime)
    - a blocking function that runs the game until it ends.
    - runs the scheduler to execute tasks
- void push_task(tick, callback, *args, **kwargs)
    - push a task to the task queue
- void level_up_task()
    - task to level up the game
- void game_over_task()
    - task to end the game
    - also clears the scheduler
- vodi game_end() **(abstract)**
    - notify the players that the game is over
- void push_new_row_task() **(abstract)**
    - task to push new row to the game board
- void set_player_callback(callback cb, int player_id=1) **(abstract)**
    - sets the callback function to be called when the player can take action
- bool check_player_callback() **(abstract)**
    - check if all required callbacks are set
- void player_callback_task(int player_id) **(abstract)**
    - handles player callback
- void init_tasks() **(virtual)**
    - initialize level up and push new row tasks
- void get_tick_between_new_row() **(virtual)**
    - returns the tick between each new row task
- void get_tick_between_level_up() **(virtual)**
    - returns the tick between each level up task

## Endless1PGameState (GameState)
### var
- GameBoardState game_board_state
- float empty_row_percentage = 0.8
- callback player_callback
### methods
- Endless1PGameState(GameBoardState game_board_state, int player_swap_delay, int player_select_delay, float empty_row_percentage=0.8)
- void push_new_row_task() **(override)**
- bool check_player_callback() **(override)**
    - check if player_callback is set
- void set_player_callback(callback cb, int player_id=1) **(override)**
- void player_callback_task(int player_id) **(override)**
    - handle player callback
- void init_tasks() **(override)**
    - needs to call super().init_tasks()
    - push load_task()
    - push task for player 1 to take action
- void game_end() **(override)**
    - notify the player that the game is over
- void load_task()
    - task to load the game board with ramdom numbers

## VersusGameState (GameState)
### PlayerState (subclass)
#### var
- GameBoardState game_board_state
- VersusGameState game_state
- int last_pressure_tick = 0
- const int PRESSURE_TICK_DURATION = 120
- const int MAX_PRESSURE_PER_ATTACK = 20
- const int GARBAGE_PER_ADDITIONAL_ROW = 10
#### method
- PlayerState(VersusGameState game_state, GameBoardState game_board_state)
- void reset_pressure_tick()
- void attack(score_increase_info)
    - needs to be called by GameScoreState when score increases
- int compute_attack_power(score_increase_info)
- (int, int) compute_attack_load(int garbage)
    - returns (num_rows, num_columns)
- void load_task()
    - task to load the game board with ramdom numbers
- void check_recieve_garbage_task()
    - check if the player needs to recieve garbage from pressure?
### main class
#### var
- List[PlayerState] player_states
#### method
- void register_player(GameBoardState game_board_state)
    - register a new player
- PlayerState find_target(PlayerState attacker) **(virtual)**
    - find a valid target for the attacker
- void on_draw() **(abstract)**
- void check_game_result_state() **(virtual)**
    - Method to invoke to check if the game has been decided
- void push_new_row_task() **(override)**
    - VersusGameState's PushNewRowEvent implementation. Uses PlayerState.
- bool check_player_callback() **(override)** ???
    - check if all player callbacks are set
- void set_player_callback(callback cb, int player_id=1) **(override)** ???
    - set the callback for the player
- void player_callback_task(int player_id) **(override)** ???

## Endless2PGameState (VersusGameState)
### var
### method
- Endless2PGameState(
    GameBoardState p1_game_board_state, 
    GameBoardState p2_game_board_state
    )
- int get_tick_between_new_row() **(override)**
    - rows appear less frequently in 2P mode
- void on_draw() **(override)**

---

## GameBoardState
### var
- dict config {
    - int seed
    - int row_count, column_count
    - int number_upper_bound
    - int minimum_sorted_length
    - int base_remove_score
    - int remove_length_bonus
    - int max_effective_combo
    - float combo_score_step
}
- GameGridState game_grid_state
- np.random_instance
- GameControllerState game_controller_state
- GameScoreState game_score_state
- GamePressureState gamePressureState
### method
- GameBoardState(dict config)
- bool push_new_row(int number_of_columns)
- bool push_garbage_rows(int number_of_rows, int number_of_columns)

## GameTileState
### const
- EMPTY = -1
- GARBAGE = -2
### var
- number
### method
- GameTileState(int val = EMPTY)
- is_empty()
- is_garbage()
- is_number()

## GameGridState
### var
- row_count
- column_count
- number_upper_bound
    - upper bound of the tile number in the grid
- grid
    - 2D-list of GameTileState
### method
- GameGridState(int row_count, int column_count, number_upper_bound)
    - initialize to -1 (Empty)
- copy(other) # copy constructor (classmethod!)
- void inplace_copy(GameGridState other)
- int get(Coord coord)
- void set(Coord coord, int value)
- bool is_empty(Coord coord)
- bool is_garbage(Coord coord)
- bool is_number(Coord coord)
- void clear() # flush to -1
- void load_random(float empty_row_percentage)
    - empty_row_percentage: the percentage of rows that are empty tiles
    - the random numbers are generated from 0 to number_upper_bound "[0, number_upper_bound)"
- void load_row(int row_id, list row_values)
- void load_column(int column_id, list column_values)
- void load_grid(list grid_values) # gridValues is a 2D-list
- void pull_down(int column)
- void swap(Coord coord1, Coord coord2)
- void swap_and_pull_down(Coord coord1, Coord coord2)
- bool push_up(int column, int number) # returns whether the grid has overflowed
- void remove_tiles(list[Coord] coords)
- bool content_equal(GameGridState other)

## GameControllerState
### var
- GameGridState game_grid_state (from gameBoardState)
- GameScoreState game_score_state (from gameBoardState)
- int minimum_sorted_length
- SelectHandler selecter
- SwapHandler swaper
### method
- GameControllerState(GameGridState game_grid_state, GameScoreState game_score_state, int minimum_sorted_length)
- (int, int) select(list[Coord]) # call selector, and send result to gameScoreState
- bool swap(list[Coord]) # call swaper

## SelectHandler
### method
- SelectHandler(GameGridState game_grid_state, minimum_sorted_length)
- (int, int) select(list[Coords] coords)
    - This method should check valid, and call functions in gameGridState to remove tiles
    - returns (remove number tiles count, remove garbage tiles count)
## SwapHandler
### method
- SwapHandler(GameGridState game_grid_state)
- bool swap(list[Coords] coords)
    - This method should check valid, and call functions in gameGridState to swap tiles
    - returns True is successfully swap, False otherwise

## GameScoreState
### var
- int total_score
- int combo
- int effective_combo
- int combo_score_buffer
- dict config {
    int minimum_remove_count, base_remove_score, max_effective_combo, remove_length_bonus
    float combo_score_step
}
### method
- GameScoreState(dict config)
- void on_remove(int remove_count)

## GamePressureState
### var
- int pressure
- int max_pressure
- ~~float pressure_rate~~ (probably for unity, tedious to maintain in python)
### method
- GamePressureState(int max_pressure=40)
- int consume_pressure(int amount)
- void add_pressure(int amount)
- void attack(GamePressureState other, int attackPower)
- float get_pressure_rate() # in case anyone need pressure_rate