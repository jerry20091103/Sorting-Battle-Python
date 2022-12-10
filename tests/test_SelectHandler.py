from sorting_battle_gym.select_handler import SelectHandler
from sorting_battle_gym.game_grid_state import GameGridState

class TestSelectHandler:
    '''
    Tests for SelectHandler class.
    GameGridState is required to test SelectHandler.
    '''
    def test_vertical_decreasing_selection(self):
        '''
        Test a valid vertical decreasing selection.
        '''
        input_case = [[-1, -1, -1, -1, -1],
                      [-1,  7, -1, -1, -1],
                      [-1,  6, -1, -1, -1],
                      [-1,  5, -1, -1, -1],
                      [-1,  4, -1, -1, -1]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        select_handler = SelectHandler(grid_state, 3)
        assert select_handler.select([(1, 1), (2, 1), (3, 1), (4, 1)]) == (4, 0)
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1]]
        grid_answer = GameGridState(5, 5)
        grid_answer.load_grid(answer)
        assert grid_state.content_equal(grid_answer)

    def test_horizontal_increasing_selection(self):
        '''
        Test a valid horizontal increasing selection.
        '''
        input_case = [[-1, -1, -1, -1, -1],
                      [-1,  7, -1, -1, -1],
                      [ 2,  6, -1, -1, -1],
                      [15,  5, -1,  6, -1],
                      [ 1,  4,  5, 12, 13]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        select_handler = SelectHandler(grid_state, 3)
        assert select_handler.select([(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]) == (5, 0)
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1,  7, -1, -1, -1],
                  [ 2,  6, -1, -1, -1],
                  [15,  5, -1,  6, -1]]
        grid_answer = GameGridState(5, 5)
        grid_answer.load_grid(answer)
        assert grid_state.content_equal(grid_answer)

    def test_not_sorted_selection(self):
        '''
        Test a selection that is not sorted. This should be invalid.
        '''
        input_case = [[-1, -1, -1, -1, -1],
                      [-1,  7, -1, -1, -1],
                      [-1,  6, -1, -1, -1],
                      [-1,  5, -1,  6, -1],
                      [-1,  4,  5, 12, 13]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        select_handler = SelectHandler(grid_state, 3)
        assert select_handler.select([(3, 1), (3, 2), (3, 3)]) == (0, 0)
        grid_answer = GameGridState(5, 5)
        grid_answer.load_grid(input_case)
        assert grid_state.content_equal(grid_answer)
    
    def test_short_selection(self):
        '''
        Test a selection that is less than minimum_sorted_length. This should be invalid.
        '''
        input_case = [[-1, -1, -1, -1, -1],
                      [-1,  7, -1, -1, -1],
                      [-1,  6, -1, -1, -1],
                      [-1,  5, -1,  6, -1],
                      [-1,  4,  5, 12, 13]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        select_handler = SelectHandler(grid_state, 3)
        assert select_handler.select([(4, 3), (4, 4)]) == (0, 0)
        grid_answer = GameGridState(5, 5)
        grid_answer.load_grid(input_case)
        assert grid_state.content_equal(grid_answer)
    
    def test_diagonal_selection(self):
        '''
        Test a diagonal selection. This should be invalid.
        '''
        input_case = [[-1, -1,  9, -1,  1],
                      [-1,  7,  8, -1,  2],
                      [ 2,  6,  3, -1,  3],
                      [15,  5,  2,  5,  4],
                      [ 1,  4,  5,  6,  5]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        select_handler = SelectHandler(grid_state, 3)
        assert select_handler.select([(2, 0), (1, 1), (0, 3)]) == (0, 0)
        grid_answer = GameGridState(5, 5)
        grid_answer.load_grid(input_case)
        assert grid_state.content_equal(grid_answer)
    
    def test_out_of_order_selection(self):
        '''
        Test a selection that is not along a vertical or horizontal line. 
        This should be invalid.
        '''
        input_case = [[-1, -1,  9, -1,  1],
                      [-1,  7,  8, -1,  2],
                      [ 2,  6,  3, -1,  3],
                      [15,  5,  2,  5,  4],
                      [ 1,  4,  5,  6,  5]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        select_handler = SelectHandler(grid_state, 3)
        assert select_handler.select([(3, 1), (3, 2), (3, 0)]) == (0, 0)
        grid_answer = GameGridState(5, 5)
        grid_answer.load_grid(input_case)
        assert grid_state.content_equal(grid_answer)
    
    def test_non_decreasing_selection(self):
        '''
        Test a valid selection that has the same number tiles in a row.
        '''
        input_case = [[-1, -1,  9, -1,  1],
                      [-1,  7,  8, -1,  2],
                      [ 2,  6,  3, -1,  3],
                      [15,  5,  5,  6,  6],
                      [ 1,  4,  5,  6,  5]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        select_handler = SelectHandler(grid_state, 3)
        assert select_handler.select([(3, 1), (3, 2), (3, 3), (3, 4)]) == (4, 0)
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1,  9, -1,  1],
                  [ 2,  7,  8, -1,  2],
                  [15,  6,  3, -1,  3],
                  [ 1,  4,  5,  6,  5],]
        grid_answer = GameGridState(5, 5)
        grid_answer.load_grid(answer)
        assert grid_state.content_equal(grid_answer)
    
    def test_repeated_selection(self):
        '''
        Test a selection that has repeated tile coordinates.
        This should be invalid.
        '''
        input_case = [[-1, -1,  9, -1,  1],
                      [-1,  7,  8, -1,  2],
                      [ 2,  6,  3, -1,  3],
                      [15,  5,  5,  6,  6],
                      [ 1,  4,  5,  6,  5]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        select_handler = SelectHandler(grid_state, 3)
        assert select_handler.select([(4, 1), (4, 2), (4, 2), (4, 3)]) == (0, 0)
        grid_answer = GameGridState(5, 5)
        grid_answer.load_grid(input_case)
        assert grid_state.content_equal(grid_answer)
    
    def test_empty_selection(self):
        '''
        Test an empty selection.
        This should be invalid.
        '''
        input_case = [[-1, -1,  9, -1,  1],
                      [-1,  7,  8, -1,  2],
                      [ 2,  6,  3, -1,  3],
                      [15,  5,  5,  6,  6],
                      [ 1,  4,  5,  6,  5]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        select_handler = SelectHandler(grid_state, 3)
        assert select_handler.select([]) == (0, 0)
        grid_answer = GameGridState(5, 5)
        grid_answer.load_grid(input_case)
        assert grid_state.content_equal(grid_answer)
    
    def test_select_empty_tiles(self):
        '''
        Test a selection that has empty tiles.
        This should be invalid.
        '''
        input_case = [[-1, -1,  9, -1,  1],
                      [-1,  7,  8, -1,  2],
                      [ 2,  6,  3, -1,  3],
                      [15,  5,  5,  6,  6],
                      [ 1,  4,  5,  6,  5]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        select_handler = SelectHandler(grid_state, 3)
        assert select_handler.select([(1, 0), (2, 0), (3, 0)]) == (0, 0)
        grid_answer = GameGridState(5, 5)
        grid_answer.load_grid(input_case)
        assert grid_state.content_equal(grid_answer)
    
    def test_remove_garbage_horizontal(self):
        '''
        Garbage tiles ajacent to the selection should be removed. 
        (only vertical and horizontal, not diagonal ones)
        '''
        input_case = [[-1, -1, -1, -1, -1],
                      [-1,  7, -1, -1, -2],
                      [-1,  6, -2, -1,  9],
                      [-2,  5,  6,  7,  8],
                      [-2,  4, -2, -2, -2]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        select_handler = SelectHandler(grid_state, 3)
        # remove 4 numbers and 5 garbage tiles
        assert select_handler.select([(3, 1), (3, 2), (3, 3), (3, 4)]) == (4, 5)
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1,  7, -1, -1, -1],
                  [-1,  6, -1, -1, -2],
                  [-2,  4, -1, -1,  9]]
        grid_answer = GameGridState(5, 5)
        grid_answer.load_grid(answer)
        assert grid_state.content_equal(grid_answer)

    def test_remove_garbage_vertical(self):
        '''
        Garbage tiles ajacent to the selection should be removed. 
        (only vertical and horizontal, not diagonal ones)
        '''
        input_case = [[-1, -2, -1, -1, -1],
                      [-1,  7, -1, -1, -2],
                      [-1,  6, -2, -1,  9],
                      [-2,  5,  6,  7,  8],
                      [-2,  -2, -2, -2, -2]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        select_handler = SelectHandler(grid_state, 3)
        # remove 3 numbers and 4 garbage tiles
        assert select_handler.select([(1, 1), (2, 1), (3, 1)]) == (3, 4)
        answer = [[-1, -1, -1, -1, -1],
                  [-1,  -1, -1, -1, -2],
                  [-1,  -1, -1, -1,  9],
                  [-1,  -1,  6,  7,  8],
                  [-2,  -1, -2, -2, -2]]
        grid_answer = GameGridState(5, 5)
        grid_answer.load_grid(answer)
        assert grid_state.content_equal(grid_answer)

