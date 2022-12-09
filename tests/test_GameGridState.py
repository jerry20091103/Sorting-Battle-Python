from sorting_battle_gym.game_grid_state import GameGridState
import numpy as np

class TestGameGridState:
    def test_constructor(self):
        '''
        Test the constructor of GameGridState.
        Check that all tiles are initilized to -1.
        '''
        cases = [(2, 3), (3, 4), (4, 5), (5, 6)]
        for case in cases:
            state = GameGridState(case[0], case[1])
            for i in range(case[0]):
                for j in range(case[1]):
                    assert state.get((i, j)) == -1
    
    def test_get_set(self):
        '''
        Test the get and set functions of GameGridState.
        '''
        cases = [(2, 3), (3, 4), (4, 5), (5, 6)]
        for case in cases:
            state = GameGridState(case[0], case[1])
            # creatre random matrix
            matrix = np.random.randint(0, 99, (case[0], case[1]))
            for i in range(case[0]):
                for j in range(case[1]):
                    state.set((i, j), matrix[i, j])
            for i in range(case[0]):
                for j in range(case[1]):
                    assert state.get((i, j)) == matrix[i, j]
    
    def test_content_equal(self):
        '''
        Test the content_equal method of GameGridState.
        '''
        cases = [(3, 4), (4, 5)]
        for case in cases:
            stateA = GameGridState(case[0], case[1])
            stateB = GameGridState(case[0], case[1])
            # create random matrix
            matrix = np.random.randint(0, 99, (case[0], case[1]))
            for i in range(case[0]):
                for j in range(case[1]):
                    stateA.set((i, j), matrix[i, j])
                    stateB.set((i, j), matrix[i, j])
            assert stateA.content_equal(stateB)
            stateA.set((0, 0), -1)
            assert not stateA.content_equal(stateB)
            assert not stateA.content_equal(GameGridState(case[0], case[1]))

    def test_copy(self):
        '''
        Test the inplace_copy method and copy constructor of GameGridState.
        '''
        cases = [(3, 4), (4, 5)]
        for case in cases:
            stateA = GameGridState(case[0], case[1])
            stateB = GameGridState(case[0], case[1])
            stateB.load_random()
            stateA.inplace_copy(stateB)
            assert stateA.content_equal(stateB)
            stateB.load_random()
            stateC = GameGridState.copy(stateB)
            assert stateC.content_equal(stateB)

    def test_clear(self):
        '''
        Test the clear method of GameGridState.
        '''
        cases = [(3, 4), (4, 5)]
        for case in cases:
            state = GameGridState(case[0], case[1])
            state.load_random()
            for i in range(case[0]):
                for j in range(case[1]):
                    assert state.get((i, j)) != -1
            state.clear()
            for i in range(case[0]):
                for j in range(case[1]):
                    assert state.get((i, j)) == -1
    
    def test_swap(self):
        '''
        Test the swap method of GameGridState.
        '''
        x1 = [0, 1, 2]
        y1 = [0, 1, 2]
        x2 = [0, 1, 2]  
        y2 = [0, 1, 2]
        state = GameGridState(3, 3)
        state.load_random()
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        p1 = (x1[i], y1[j])
                        p2 = (x2[k], y2[l])
                        val1 = state.get(p1)
                        val2 = state.get(p2)
                        state.swap(p1, p2)
                        assert state.get(p1) == val2
                        assert state.get(p2) == val1

    def test_load_random(self):
        '''
        Test the load_random method of GameGridState.
        '''
        state = GameGridState(10, 5)
        percentage = 0
        for i in range(10):
            percentage += 0.1
            state.load_random(percentage)
            for row in range(0, 10 - percentage*10):
                for col in range(0, 5):
                    assert state.get((row, col)) == -1
            for row in range(10 - percentage*10, 10):
                for col in range(0, 5):
                    assert state.get((row, col)) != -1