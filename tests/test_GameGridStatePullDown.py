from sorting_battle_gym.GameGridState import GameGridState

class TestGameGridStatePullDown:
    def test_PullDown_case1(self):
        '''
        Test the PullDown method of GameGridState.
        '''
        inputCase = [[-1, -1, -1, -1, -1],
                     [-1, -1,  5, -1,  5],
                     [-1, -1,  4, -1,  5],
                     [-1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase = stateCase.LoadGrid(inputCase)
        stateCase.PullDown(2)
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1,  5],
                  [-1, -1, -1, -1,  5],
                  [-1, -1,  5, -1, -1],
                  [-1, -1,  4, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer = stateAnswer.LoadGrid(answer)
        assert stateCase.ContentEqual(stateAnswer)
    
    def test_PullDown_case2(self):
        '''
        Test the PullDown method of GameGridState.
        '''
        state = GameGridState(5, 5)
        state.PullDown(1)
        assert state.ContentEqual(GameGridState(5, 5))
    
    def test_PullDown_case3(self):
        '''
        Test the PullDown method of GameGridState.
        '''
        inputCase = [[-1,  6, -1, -1, -1],
                     [-1,  5, -1, -1, -1],
                     [-1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1],
                     [-1,  1, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase = stateCase.LoadGrid(inputCase)
        stateCase.PullDown(1)
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1,  6, -1, -1, -1],
                  [-1,  5, -1, -1, -1],
                  [-1,  1, -1, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer = stateAnswer.LoadGrid(answer)
        assert stateCase.ContentEqual(stateAnswer)
    
    def test_SwapAndPullDown_case1(self):
        '''
        Test the SwapAndPullDown method of GameGridState.
        '''
        inputCase = [[-1, -1, -1, -1, -1],
                     [-1,  7, -1, -1, -1],
                     [-1,  6, -1, -1, -1],
                     [-1,  5, -1, -1, -1],
                     [-1,  4, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase = stateCase.LoadGrid(inputCase)
        stateCase.SwapAndPullDown((3, 1), (3, 2))
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1,  7, -1, -1, -1],
                  [-1,  6, -1, -1, -1],
                  [-1,  4,  5, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer = stateAnswer.LoadGrid(answer)
        assert stateCase.ContentEqual(stateAnswer)

    def test_SwapAndPullDown_case2(self):
        '''
        Test the SwapAndPullDown method of GameGridState.
        '''
        inputCase = [[-1, -1, -1, -1, -1],
                     [-1,  7, -1, -1, -1],
                     [-1,  6, -1, -1, -1],
                     [-1,  5, -1, -1, -1],
                     [-1,  4, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase = stateCase.LoadGrid(inputCase)
        stateCase.SwapAndPullDown((1, 1), (1, 2))
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1,  6, -1, -1, -1],
                  [-1,  5, -1, -1, -1],
                  [-1,  4,  7, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer = stateAnswer.LoadGrid(answer)
        assert stateCase.ContentEqual(stateAnswer)
    
    def test_SwapAndPullDown_case3(self):
        '''
        Test the SwapAndPullDown method of GameGridState.
        '''
        inputCase = [[-1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1],
                     [ 1, -1, -1, -1, -1],
                     [ 2,  5, -1, -1, -1],
                     [ 3,  4, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase = stateCase.LoadGrid(inputCase)
        stateCase.SwapAndPullDown((3, 0), (3, 1))
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [ 1, -1, -1, -1, -1],
                  [ 5,  2, -1, -1, -1],
                  [ 3,  4, -1, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer = stateAnswer.LoadGrid(answer)
        assert stateCase.ContentEqual(stateAnswer)
        stateCase.SwapAndPullDown((2, 0), (2, 1))
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1,  1, -1, -1, -1],
                  [ 5,  2, -1, -1, -1],
                  [ 3,  4, -1, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer = stateAnswer.LoadGrid(answer)
        assert stateCase.ContentEqual(stateAnswer)
    
    def test_SwapAndPullDown_case4(self):
        '''
        Test the SwapAndPullDown method of GameGridState.
        '''
        inputCase = [[-1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1],
                     [ 1, -1, -1, -1, -1],
                     [ 2,  5, -1, -1, -1],
                     [ 3,  4, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase = stateCase.LoadGrid(inputCase)
        stateCase.SwapAndPullDown((4, 2), (4, 3))
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [ 1, -1, -1, -1, -1],
                  [ 2,  5, -1, -1, -1],
                  [ 3,  4, -1, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer = stateAnswer.LoadGrid(answer)
        assert stateCase.ContentEqual(stateAnswer)
        
        

        