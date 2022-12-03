from sorting_battle_gym.GameGridState import GameGridState
import numpy as np

class TestGameGridState:
    def test_Constructor(self):
        '''
        Test the constructor of GameGridState.
        Check that all tiles are initilized to -1.
        '''
        cases = [(2, 3), (3, 4), (4, 5), (5, 6)]
        for case in cases:
            state = GameGridState(case[0], case[1])
            for i in range(case[0]):
                for j in range(case[1]):
                    assert state.Get((i, j)) == -1
    
    def test_GetSet(self):
        '''
        Test the Get and Set functions of GameGridState.
        '''
        cases = [(2, 3), (3, 4), (4, 5), (5, 6)]
        for case in cases:
            state = GameGridState(case[0], case[1])
            # creatre random matrix
            matrix = np.random.randint(0, 99, (case[0], case[1]))
            for i in range(case[0]):
                for j in range(case[1]):
                    state.Set((i, j), matrix[i, j])
            for i in range(case[0]):
                for j in range(case[1]):
                    assert state.Get((i, j)) == matrix[i, j]
    
    def test_ContentEqual(self):
        '''
        Test the ContentEqual method of GameGridState.
        '''
        cases = [(3, 4), (4, 5)]
        for case in cases:
            stateA = GameGridState(case[0], case[1])
            stateB = GameGridState(case[0], case[1])
            # create random matrix
            matrix = np.random.randint(0, 99, (case[0], case[1]))
            for i in range(case[0]):
                for j in range(case[1]):
                    stateA.Set((i, j), matrix[i, j])
                    stateB.Set((i, j), matrix[i, j])
            assert stateA.ContentEqual(stateB)
            stateA.Set((0, 0), -1)
            assert not stateA.ContentEqual(stateB)
            assert not stateA.contentEqual(GameGridState(case[0], case[1]))

    def test_Copy(self):
        '''
        Test the InplaceCopy method and copy constructor of GameGridState.
        '''
        cases = [(3, 4), (4, 5)]
        for case in cases:
            stateA = GameGridState(case[0], case[1])
            stateB = GameGridState(case[0], case[1])
            stateB.LoadRandom()
            stateA.InplaceCopy(stateB)
            assert stateA.ContentEqual(stateB)
            stateB.LoadRandom()
            stateC = GameGridState.copy(stateB)
            assert stateC.ContentEqual(stateB)

    def test_Clear(self):
        '''
        Test the Clear method of GameGridState.
        '''
        cases = [(3, 4), (4, 5)]
        for case in cases:
            state = GameGridState(case[0], case[1])
            state.LoadRandom()
            for i in range(case[0]):
                for j in range(case[1]):
                    assert state.Get((i, j)) != -1
            state.Clear()
            for i in range(case[0]):
                for j in range(case[1]):
                    assert state.Get((i, j)) == -1
    
    def test_Swap(self):
        '''
        Test the Swap method of GameGridState.
        '''
        x1 = [0, 1, 2]
        y1 = [0, 1, 2]
        x2 = [0, 1, 2]  
        y2 = [0, 1, 2]
        state = GameGridState(3, 3)
        state.LoadRandom()
        for i in range(3):
            p1 = (x1[i], y1[i])
            p2 = (x2[i], y2[i])
            val1 = state.Get(p1)
            val2 = state.Get(p2)
            state.Swap(p1, p2)
            assert state.Get(p1) == val2
            assert state.Get(p2) == val1