from sorting_battle_gym.game_grid_state import GameTileState

class TestGameTileState:
    def test_constructor(self):
        '''
        Test the constructor of GameTileState.
        '''
        cases = [0, 1, 2, -1, -2]
        for case in cases:
            state = GameTileState(case)
            assert state.val == case
        state = GameTileState()
        assert state.val == -1

    def test_is_empty(self):
        '''
        Test the is_empty method of GameTileState.
        '''
        cases = [0, 1, 2, -2]
        for case in cases:
            state = GameTileState(case)
            assert state.is_empty() == False
        
        state = GameTileState(-1)
        assert state.is_empty()
        state = GameTileState()
        assert state.is_empty()

    def test_is_garbage(self):
        '''
        Test the is_garbage method of GameTileState.
        '''
        cases = [0, 1, 2, -1]
        for case in cases:
            state = GameTileState(case)
            assert state.is_garbage() == False
        
        state = GameTileState(-2)
        assert state.is_garbage()
        state = GameTileState()
        assert state.is_garbage() == False

    def test_is_number(self):
        '''
        Test the is_number method of GameTileState.
        '''
        cases = [-1, -2]
        for case in cases:
            state = GameTileState(case)
            assert state.is_number() == False
        
        state = GameTileState(0)
        assert state.is_number()
        state = GameTileState(1)
        assert state.is_number()
        state = GameTileState(2)
        assert state.is_number()
        state = GameTileState()
        assert state.is_number() == False