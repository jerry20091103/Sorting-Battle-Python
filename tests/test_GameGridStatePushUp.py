from sorting_battle_gym.GameGridState import GameGridState

class TestGameGridStatePushUp:
    def test_PushUpWithNoOverflow(self):
        '''
        Test the PushUp method of GameGridState.
        '''
        inputCase = [[-1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1],
                     [ 1, -1, -1, -1, -1],
                     [ 2,  5, -1, -1, -1],
                     [ 3,  4, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase = stateCase.LoadGrid(inputCase)
        overflow = stateCase.PushUp(0, 4)
        assert not overflow
        answer = [[-1, -1, -1, -1, -1],
                  [ 1, -1, -1, -1, -1],
                  [ 2, -1, -1, -1, -1],
                  [ 3,  5, -1, -1, -1],
                  [ 4,  4, -1, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer = stateAnswer.LoadGrid(answer)
        assert stateCase.ContentEqual(stateAnswer)
    
    def test_PushUpWithOverflow(self):
        '''
        Test the PushUp method of GameGridState.
        '''
        inputCase = [[ 1, -1, -1, -1, -1],
                     [ 2, -1, -1, -1, -1],
                     [ 3, -1, -1, -1, -1],
                     [ 4,  5, -1, -1, -1],
                     [ 5,  4, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase = stateCase.LoadGrid(inputCase)
        overflow = stateCase.PushUp(0, 6)
        assert overflow
        answer = [[ 2, -1, -1, -1, -1],
                  [ 3, -1, -1, -1, -1],
                  [ 4, -1, -1, -1, -1],
                  [ 5,  5, -1, -1, -1],
                  [ 6,  4, -1, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer = stateAnswer.LoadGrid(answer)
        assert stateCase.ContentEqual(stateAnswer)