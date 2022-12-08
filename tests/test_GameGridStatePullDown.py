from sorting_battle_gym.game_grid_state import GameGridState

class TestGameGridStatePullDown:
    def test_pull_down_case1(self):
        '''
        Test the pull_down method of GameGridState.
        '''
        inputCase = [[-1, -1, -1, -1, -1],
                     [-1, -1,  5, -1,  5],
                     [-1, -1,  4, -1,  5],
                     [-1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase.load_grid(inputCase)
        stateCase.pull_down(2)
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1,  5],
                  [-1, -1, -1, -1,  5],
                  [-1, -1,  5, -1, -1],
                  [-1, -1,  4, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer.load_grid(answer)
        assert stateCase.content_equal(stateAnswer)
    
    def test_pull_down_case2(self):
        '''
        Test the PullDown method of GameGridState.
        '''
        state = GameGridState(5, 5)
        state.pull_down(1)
        assert state.content_equal(GameGridState(5, 5))
    
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
        stateCase.load_grid(inputCase)
        stateCase.pull_down(1)
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1,  6, -1, -1, -1],
                  [-1,  5, -1, -1, -1],
                  [-1,  1, -1, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer.load_grid(answer)
        assert stateCase.content_equal(stateAnswer)
    
    def test_swap_and_pull_down_case1(self):
        '''
        Test the swap_and_pull_down method of GameGridState.
        '''
        inputCase = [[-1, -1, -1, -1, -1],
                     [-1,  7, -1, -1, -1],
                     [-1,  6, -1, -1, -1],
                     [-1,  5, -1, -1, -1],
                     [-1,  4, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase.load_grid(inputCase)
        stateCase.swap_and_pull_down((3, 1), (3, 2))
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1,  7, -1, -1, -1],
                  [-1,  6, -1, -1, -1],
                  [-1,  4,  5, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer.load_grid(answer)
        assert stateCase.content_equal(stateAnswer)

    def test_swap_and_pull_down_case2(self):
        '''
        Test the swap_and_pull_down method of GameGridState.
        '''
        inputCase = [[-1, -1, -1, -1, -1],
                     [-1,  7, -1, -1, -1],
                     [-1,  6, -1, -1, -1],
                     [-1,  5, -1, -1, -1],
                     [-1,  4, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase.load_grid(inputCase)
        stateCase.swap_and_pull_down((1, 1), (1, 2))
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1,  6, -1, -1, -1],
                  [-1,  5, -1, -1, -1],
                  [-1,  4,  7, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer.load_grid(answer)
        assert stateCase.content_equal(stateAnswer)
    
    def test_swap_and_pull_down_case3(self):
        '''
        Test the swap_and_pull_down method of GameGridState.
        '''
        inputCase = [[-1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1],
                     [ 1, -1, -1, -1, -1],
                     [ 2,  5, -1, -1, -1],
                     [ 3,  4, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase.load_grid(inputCase)
        stateCase.swap_and_pull_down((3, 0), (3, 1))
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [ 1, -1, -1, -1, -1],
                  [ 5,  2, -1, -1, -1],
                  [ 3,  4, -1, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer.load_grid(answer)
        assert stateCase.content_equal(stateAnswer)
        stateCase.swap_and_pull_down((2, 0), (2, 1))
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [-1,  1, -1, -1, -1],
                  [ 5,  2, -1, -1, -1],
                  [ 3,  4, -1, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer.load_grid(answer)
        assert stateCase.content_equal(stateAnswer)
    
    def test_swap_and_pull_down_case4(self):
        '''
        Test the swap_and_pull_down method of GameGridState.
        '''
        inputCase = [[-1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1],
                     [ 1, -1, -1, -1, -1],
                     [ 2,  5, -1, -1, -1],
                     [ 3,  4, -1, -1, -1]]
        stateCase = GameGridState(5, 5)
        stateCase.load_grid(inputCase)
        stateCase.swap_and_pull_down((4, 2), (4, 3))
        answer = [[-1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1],
                  [ 1, -1, -1, -1, -1],
                  [ 2,  5, -1, -1, -1],
                  [ 3,  4, -1, -1, -1]]
        stateAnswer = GameGridState(5, 5)
        stateAnswer.load_grid(answer)
        assert stateCase.content_equal(stateAnswer)
        
        

        