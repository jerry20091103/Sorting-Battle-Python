# Sorting Battle Code Structure
## GameState
### var
- dict config {
    - int player_count
}
- GameBoardStatse game_board_state
### method
#### These are public methods to call from outisde (the RL model)
- GameState(dict config)
- set_callback(callback cb, int player_id=1) 
    - sets the callback function to be called when the player can take action
    - todo: define the callback function interface
- void run_game()
    - a blocking function that runs the game until it ends.

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
- void load_random(float row_percentage)
    - row_percentage: the percentage of rows that are filled with random numbers (leave the rest empty)
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
- bool swap(Coord coord1, Coord coord2) # call swaper

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
### TODO
