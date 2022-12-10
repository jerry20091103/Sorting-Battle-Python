from sorting_battle_gym.game_controller_state import GameControllerState
from sorting_battle_gym.game_score_state import GameScoreState
from sorting_battle_gym.game_grid_state import GameGridState

class TestGameControllerState:
    def test_integration_case1(self):
        '''
        Test the integration of GameControllerState.
        '''
        input_case = [[-1, -1,  2, -1, -1],
                      [-1, -1,  6,  4, -1],
                      [-1,  1, 54,  7, -1],
                      [ 5,  2, 14, 11, 66],
                      [ 3,  4, 22, 12, 88]]
        grid_state = GameGridState(5, 5)
        grid_state.load_grid(input_case)
        config = {
            'minimum_remove_count': 3,
            'base_remove_score': 50,
            'max_effective_combo': 10,
            'remove_length_bonus': 25,
            'combo_score_step': 2.0,}
        score_state = GameScoreState(config)
        controller_state = GameControllerState(grid_state, score_state, 3)
        grid_answer = GameGridState(5, 5)
        # try a successful horizontal swap
        assert controller_state.swap([(4, 3), (4, 2)]) == True
        answer = [[-1, -1,  2, -1, -1],
                  [-1, -1,  6,  4, -1],
                  [-1,  1, 54,  7, -1],
                  [ 5,  2, 14, 11, 66],
                  [ 3,  4, 12, 22, 88]]
        grid_answer.load_grid(answer)
        assert grid_state.content_equal(grid_answer)
        # try a successful vertical swap
        assert controller_state.swap([(3, 0), (4, 0)]) == True
        answer = [[-1, -1,  2, -1, -1],
                  [-1, -1,  6,  4, -1],
                  [-1,  1, 54,  7, -1],
                  [ 3,  2, 14, 11, 66],
                  [ 5,  4, 12, 22, 88]]
        grid_answer.load_grid(answer)
        assert grid_state.content_equal(grid_answer)
        # try a failed swap
        assert controller_state.swap([(0, 2), (0, 3)]) == False
        assert grid_state.content_equal(grid_answer)
        # try a successful vertical swap
        assert controller_state.swap([(3, 0), (4, 0)]) == True
        answer = [[-1, -1,  2, -1, -1],
                  [-1, -1,  6,  4, -1],
                  [-1,  1, 54,  7, -1],
                  [ 5,  2, 14, 11, 66],
                  [ 3,  4, 12, 22, 88]]
        grid_answer.load_grid(answer)
        assert grid_state.content_equal(grid_answer)
        # remove the bottommost row
        assert controller_state.select([(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]) == (5, 0)
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1,  2, -1, -1],
                  [-1, -1,  6,  4, -1],
                  [-1,  1, 54,  7, -1],
                  [ 5,  2, 14, 11, 66]]
        grid_answer.load_grid(answer)
        assert grid_state.content_equal(grid_answer)
        # try a failed remove
        assert controller_state.select([(2, 2), (3, 2), (4, 2)]) == (0, 0)
        # the answer should be the same
        assert grid_state.content_equal(grid_answer)
        # try a successful remove
        assert controller_state.select([(1, 2), (2, 2), (3, 2)]) == (3, 0)
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1, -1, -1,  4, -1],
                  [-1,  1, -1,  7, -1],
                  [ 5,  2, 14, 11, 66]]
        grid_answer.load_grid(answer)
        assert grid_state.content_equal(grid_answer)
