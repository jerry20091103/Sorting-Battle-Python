from sorting_battle_gym.game_grid_state import GameGridState

class TestGameGridStateRemove:
    def test_remove_tiles(self):
        '''
        Test the remove_tiles method of GameGridState.
        '''
        inputCase = [[ 2,  6,  3, -1,  3],
                     [15,  5,  2,  5,  4],
                     [ 1,  4,  5,  6,  1]]
        stateCase = GameGridState(3, 5)
        stateCase = stateCase.load_grid(inputCase)
        stateCase.remove_tiles([(2, 0), (2, 1), (2, 2), (2, 3)])
        answer = [[-1, -1, -1, -1,  3],
                  [ 2,  6,  3, -1,  4],
                  [15,  5,  2,  5,  1]]
        stateAnswer = GameGridState(3, 5)
        stateAnswer = stateAnswer.load_grid(answer)
        assert stateCase.content_equal(stateAnswer)
        stateCase.remove_tiles([(2, 1), (1, 1)])
        answer = [[-1, -1, -1, -1,  3],
                  [ 2, -1,  3, -1,  4],
                  [15, -1,  2,  5,  1]]
        stateAnswer = GameGridState(3, 5)
        stateAnswer = stateAnswer.load_grid(answer)
        assert stateCase.content_equal(stateAnswer)