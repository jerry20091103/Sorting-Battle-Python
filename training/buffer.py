'''
This module contains Buffer for training.
'''
class Buffer():
    '''
    This is for network buffer.
    '''
    def __init__(self):
        """
        Constructor of Buffer
        """
        self.states = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.rewards_to_go = []
        self.episode_rewards = []
