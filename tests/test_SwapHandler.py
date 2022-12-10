from sorting_battle_gym.swap_handler import SwapHandler
from sorting_battle_gym.game_grid_state import GameGridState

class TestSwapHandler:
    '''
    Tests for SwapHandler class.
    GameGridState is required to test SwapHandler.
    '''
    def test_simple_swap(self):
        '''
        Swap two valid numbers.
        '''
        input_case = [[ 2,  6,  3, -1,  3],
                      [15,  5,  2,  5,  4],
                      [ 1,  4,  5,  6,  1]]
        grid_state = GameGridState(3, 5)
        grid_state.load_grid(input_case)
        swap_handler = SwapHandler(grid_state)
        assert swap_handler.swap([(2, 0), (2, 1)]) # swap() returns True on success
        answer = [[ 2,  6,  3, -1,  3],
                  [15,  5,  2,  5,  4],
                  [ 4,  1,  5,  6,  1]]
        grid_answer = GameGridState(3, 5)
        grid_answer.load_grid(answer)
        assert grid_state.content_equal(grid_answer)

    def test_swap_empty(self):
        '''
        Swap with empty tiles. This should be invalid.
        '''
        input_case = [[ 2,  6,  3, -1,  3],
                      [15,  5,  2, -1,  4],
                      [ 1,  4,  5,  6,  1]]
        grid_state = GameGridState(3, 5)
        grid_state.load_grid(input_case)
        # swap empty with number
        swap_handler = SwapHandler(grid_state)
        assert swap_handler.swap([(0, 3), (0, 2)]) == False
        grid_answer = GameGridState(3, 5)
        grid_answer.load_grid(input_case)
        assert grid_state.content_equal(grid_answer)
        # swap number with empty
        assert swap_handler.swap([(0, 4), (0, 3)]) == False
        assert grid_state.content_equal(grid_answer)
        # swap empty with empty
        assert swap_handler.swap([(0, 3), (1, 3)]) == False
        assert grid_state.content_equal(grid_answer)
    
    def test_swap_non_adjcent(self):
        '''
        Swap non-adjacent tiles. This should be invalid.
        '''
        input_case = [[ 2,  6,  3, -1,  3],
                      [15,  5,  2,  5,  4],
                      [ 1,  4,  5,  6,  1]]
        grid_state = GameGridState(3, 5)
        grid_state.load_grid(input_case)
        # swap non-adjacent tiles
        swap_handler = SwapHandler(grid_state)
        assert swap_handler.swap([(0, 0), (1, 1)]) == False
        grid_answer = GameGridState(3, 5)
        grid_answer.load_grid(input_case)
        assert grid_state.content_equal(grid_answer)
        # swap non-adjacent tiles
        assert swap_handler.swap([(0, 0), (2, 4)]) == False
        assert grid_state.content_equal(grid_answer)
        # swap non-adjacent tiles (same position)
        assert swap_handler.swap([(0, 0), (0, 0)]) == False
        assert grid_state.content_equal(grid_answer)

    def test_swap_garbage(self):
        '''
        Swap with garbage tiles. This should be invalid.
        '''
        input_case = [[ 2,  6,  3, -1,  3],
                      [15, -2, -2,  5,  4],
                      [ 1,  4,  5,  6,  1]]
        grid_state = GameGridState(3, 5)
        grid_state.load_grid(input_case)
        # swap garbage with number
        swap_handler = SwapHandler(grid_state)
        assert swap_handler.swap([(1, 1), (0, 1)]) == False
        grid_answer = GameGridState(3, 5)
        grid_answer.load_grid(input_case)
        assert grid_state.content_equal(grid_answer)
        # swap number with garbage
        assert swap_handler.swap([(1, 3), (1, 2)]) == False
        assert grid_state.content_equal(grid_answer)
        # swap garbage with garbage
        assert swap_handler.swap([(1, 1), (1, 2)]) == False
        assert grid_state.content_equal(grid_answer)
