import math
class GameScoreState:
    '''
    Represents a board's current scoring state. This includes info such as the current score and combo. 
    GameScoreState also implements the scoring algorithm.
    '''
    def __init__(self, config):
        '''
        Initialize a GameScoreState object.
        :param config: A dictionary containing the following
            'minimum_remove_count'
            'base_remove_score'
            'max_effective_combo'
            'remove_length_bonus'
            'combo_score_step'
        '''
        # init score state
        self.total_score = 0
        self.combo = 0
        self.effective_combo = 0
        self.combo_score_buffer = 0
        # load config
        self.minimum_remove_count = config['minimum_remove_count']
        self.base_remove_score = config['base_remove_score']
        self.max_effective_combo = config['max_effective_combo']
        self.remove_length_bonus = config['remove_length_bonus']
        self.combo_score_step = config['combo_score_step']

    def on_remove(self, remove_count):
        '''
        Called when a remove is made. This function updates the score state.
        :param remove_count: The number of tiles removed in the remove.
        '''
        if remove_count < self.minimum_remove_count:
            self.reset_combo()
        else:
            self.register_combo(remove_count)
    
    def register_combo(self, remove_count):
        '''
        Register a combo.
        This should not be called outside of GameScoreState.
        '''
        self.combo += 1
        self.effective_combo = min(self.combo, self.max_effective_combo)
        plus_score = math.ceil(self.effective_combo / self.combo_score_step) * \
                                 (self.base_remove_score + (remove_count - self.minimum_remove_count) * self.remove_length_bonus \
                              )
        self.total_score += plus_score
        self.combo_score_buffer += plus_score
    
    def reset_combo(self):
        '''
        Reset the combo.
        This should not be called outside of GameScoreState.
        '''
        self.combo = 0
        self.effective_combo = 0
        self.combo_score_buffer = 0