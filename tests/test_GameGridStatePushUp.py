from sorting_battle_gym.game_grid_state import GameGridState

class TestGameGridStatePushUp:
    def test_push_up_with_no_overflow(self):
        '''
        Test the push_up method of GameGridState.
        '''
        inputCase = [[-1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1],
                     [ 1, -1, -1, -1, -1],
                     [ 2,  5, -1, -1, -1],
                     [ 3,  4, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase = stateCase.load_grid(inputCase)
        overflow = stateCase.push_up(0, 4)
        assert not overflow
        answer = [[-1, -1, -1, -1, -1],
                  [ 1, -1, -1, -1, -1],
                  [ 2, -1, -1, -1, -1],
                  [ 3,  5, -1, -1, -1],
                  [ 4,  4, -1, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer = stateAnswer.load_grid(answer)
        assert stateCase.content_equal(stateAnswer)
    
    def test_push_up_with_overflow(self):
        '''
        Test the push_up method of GameGridState.
        '''
        inputCase = [[ 1, -1, -1, -1, -1],
                     [ 2, -1, -1, -1, -1],
                     [ 3, -1, -1, -1, -1],
                     [ 4,  5, -1, -1, -1],
                     [ 5,  4, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase = stateCase.load_grid(inputCase)
        overflow = stateCase.push_up(0, 6)
        assert overflow
        answer = [[ 2, -1, -1, -1, -1],
                  [ 3, -1, -1, -1, -1],
                  [ 4, -1, -1, -1, -1],
                  [ 5,  5, -1, -1, -1],
                  [ 6,  4, -1, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer = stateAnswer.load_grid(answer)
        assert stateCase.content_equal(stateAnswer)