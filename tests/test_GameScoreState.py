from sorting_battle_gym.game_score_state import GameScoreState

class TestgGameScoreState:
    def test_initial_state(self):
        '''
        Test the initial values of GameScoreState.
        '''
        config = {
            'minimum_remove_count': 3,
            'base_remove_score': 50,
            'max_effective_combo': 10,
            'remove_length_bonus': 25,
            'combo_score_step': 2.0,}
        score_state = GameScoreState(config)
        assert score_state.total_score == 0
        assert score_state.combo == 0
        assert score_state.combo_score_buffer == 0

    def test_combo(self):
        '''
        Test the combo function of GameScoreState.
        '''
        config = {
            'minimum_remove_count': 3,
            'base_remove_score': 50,
            'max_effective_combo': 10,
            'remove_length_bonus': 25,
            'combo_score_step': 2.0,}
        score_state = GameScoreState(config)
        # build a 4x combo
        score_state.on_remove(3)
        assert score_state.combo == 1
        score_state.on_remove(4)
        assert score_state.combo == 2
        score_state.on_remove(3)
        assert score_state.combo == 3
        score_state.on_remove(4)
        assert score_state.combo == 4
        # end combo
        score_state.on_remove(1)
        assert score_state.combo == 0

    def test_score(self):
        '''
        Test the score function of GameScoreState.
        '''
        # ! The scoring formula can be adjusted down the line. 
        # ! We only make sure that it's strictly increasing.
        config = {
            'minimum_remove_count': 3,
            'base_remove_score': 50,
            'max_effective_combo': 10,
            'remove_length_bonus': 25,
            'combo_score_step': 2.0,}
        score_state = GameScoreState(config)
        prev_score = score_state.total_score
        # build 15x combo
        for i in range(15):
            score_state.on_remove(3)
            assert score_state.total_score > prev_score
            prev_score = score_state.total_score
    
    def test_combo_buffer(self):
        '''
        Test the combo buffer function of GameScoreState.
        '''
        # ! The scoring formula can be adjusted down the line. 
        # ! We only make sure that it's strictly increasing.
        config = {
            'minimum_remove_count': 3,
            'base_remove_score': 50,
            'max_effective_combo': 10,
            'remove_length_bonus': 25,
            'combo_score_step': 2.0,}
        score_state = GameScoreState(config)
        # build a 10x combo
        for i in range(10):
            score_state.on_remove(4)
        assert score_state.combo == 10
        assert score_state.total_score == score_state.combo_score_buffer
        # end combo
        score_state.on_remove(2)
        assert score_state.combo == 0
        assert score_state.combo_score_buffer == 0
        # Obvious constraint: Total score must be greater than the combo score buffer after the second combo starts.
        for i in range(3):
            score_state.on_remove(3)
        assert score_state.total_score > score_state.combo_score_buffer