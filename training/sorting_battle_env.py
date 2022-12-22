import gym
from gym import Env, spaces
import numpy as np
from sorting_battle_gym.game_grid_state import GameGridState
from sorting_battle_action import SortingBattleAction
from sorting_battle_gym.swap_handler import SwapHandler
from sorting_battle_gym.select_handler import SelectHandler

class SortingBattleEnv(Env):
    '''
    The is currently a empty class to fool the testbench.
    The contents are not guaranteed to be correct.
    '''
    def __init__(self):
        '''
        Constructor of the gym.
        '''
        super(SortingBattleEnv, self).__init__()

        self.field_size = {'row': 10, 'col': 5}
        self.board = GameGridState(self.field_size['row'], self.field_size['col'])
        
        # TODO
        self.observation_shape = (0, 0, 0)
        self.observation_space = spaces.Box(low = np.zeros(self.observation_shape), 
                                            high = np.ones(self.observation_shape),
                                            dtype = np.float16)
        # TODO
        self.action_space = spaces.Discrete(0)

    @property
    def observation(self):
        '''
        Calculate observation.
        self.observation
        :return: observations
        '''
        # TODO
        position = np.array([])
        legal_actions = np.array(self.legal_actions).reshape(0, 0)
        obs = np.stack([position,legal_actions], axis = -1)
        return obs

    @property
    def legal_actions(self):
        '''
        Find legal actions.
        :return: all legal actions
        '''
        # TODO
        legal_actions = []
        return np.array(legal_actions)

    def check_game_over(self):
        '''
        Reset game environment.
        :return: somebody win (yes:1, no:0), game over or not (yes:True, no:False)
        '''
        # TODO
        return 0, False

    def reset(self):
        '''
        Reset game environment.
        '''
        # TODO
        return self.observation
    
    def render(self):
        '''
        Visualize game state.
        '''
        pass

    def step(self, action):
        '''
        Apply action.
        '''
        # TODO
        reward = 0.1
        done = False
        info = {}
        return self.observation, reward, done, {}
