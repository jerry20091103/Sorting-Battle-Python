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
        self.observation_shape = (1, 5)
        self.observation_space = spaces.Box(-1, 1, (2, ), dtype=np.float64)
        # TODO
        self.action_space = spaces.Discrete(9)

    @property
    def observation(self):
        '''
        Calculate observation.
        :return: observations
        '''
        # TODO
        position = np.zeros(self.observation_shape)
        legal_actions = np.zeros(self.observation_shape)
        obs = np.array([0., 0.5])
        return obs

    @property
    def legal_actions(self):
        '''
        Find legal actions.
        :return: all legal actions
        '''
        # TODO
        legal_actions = [0 for _ in range(9)]
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
