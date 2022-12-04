## GameBoardState
### var
- dict config {
    - int seed
    - int row_count, column_count
    - int minimum_sorted_length
    - int base_remove_score
    - int max_effective_combo
    - float combo_score_step
}
- GameGridState game_grid_state
- np.random_instance
- GameControllerState game_controller_state
- GameScoreState game_score_state
### method
- GameBoardState(dict config)

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
- grid
    - 2D-list of GameTileState
### method
- GameGridState(int row_count, int column_count) # initialize to -1 (Empty)
- copy(other) # copy constructor (classmethod!)
- void inplace_copy(GameGridState other)
- int get(tuple coord)
- void set(tuple coord, int value)
- bool is_empty(tuple coord)
- bool is_garbage(tuple coord)
- bool is_number(tuple coord)
- void clear() # flush to -1
- void load_random(int min_inclusive, int max_exclusive)
- void load_row(int row_id, list row_values)
- void load_column(int column_id, list column_values)
- void load_grid(list grid_values) # gridValues is a 2D-list
- void pull_down(int column)
- void swap(tuple coord1, tuple coord2)
- void swap_and_pull_down(tuple coord1, tuple coord2)
- bool push_up(int column, int number) # returns whether the grid has overflowed
- void remove_tiles(list[tuple] coords)
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
- int select(list[tuple]) # call selector, and send result to gameScoreState
- bool swap(list[tuple])

## SelectHandler
## SwapHandler

## GameScoreState
### var
- int total_score
- int combo
- int combo_score_buffer
- dict config {
    int minimum_remove_count, base_remove_score, max_effective_combo, remove_length_bonus
    float combo_score_step
}
### method
- GameScoreState(dict config)
- void on_remove(int remove_count)
