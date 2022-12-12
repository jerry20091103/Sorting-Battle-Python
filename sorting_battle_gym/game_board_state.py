'''
This module contains the GameBoardState class.
'''
import numpy as np
from sorting_battle_gym.game_grid_state import GameGridState
from sorting_battle_gym.game_score_state import GameScoreState
from sorting_battle_gym.game_controller_state import GameControllerState
from sorting_battle_gym.game_pressure_state import GamePressureState

class GameBoardState:
    '''
    GameBoardState represents a board. A game can have multiple boards.
    '''
    def __init__(self, config):
        '''
        Initialize a GameBoardState object.
        :param config: A dictionary containing the following
            'seed'
            'row_count'
            'column_count'
            'number_upper_bound'
            'minimum_sorted_length'
            'base_remove_score'
            'remove_length_bonus'
            'max_effective_combo'
            'combo_score_step'
        '''
        # load init board
        if config['seed'] is not None:
            np.random.seed(config['seed'])
        self.game_grid_state = GameGridState(
            config['row_count'],
            config['column_count'],
            config['number_upper_bound']
        )
        self.game_score_state = GameScoreState({
            'minimum_remove_count': config['minimum_sorted_length'],
            'base_remove_score': config['base_remove_score'],
            'remove_length_bonus': config['remove_length_bonus'],
            'max_effective_combo': config['max_effective_combo'],
            'combo_score_step': config['combo_score_step']
        })
        self.game_controller_state = GameControllerState(
            self.game_grid_state,
            self.game_score_state,
            config['minimum_sorted_length']
        )
        self.game_pressure_state = GamePressureState()

    def push_new_row(self, number_of_columns):
        '''
        Randomly push a new row to the board.
        :param number_of_columns: The number of columns in the new row.
        :return: whether the board has overflowed.
        '''
        assert number_of_columns <= self.game_grid_state.column_count, 'number_of_columns must be less than or equal to column_count'
        columns = np.random.choice(self.game_grid_state.column_count, number_of_columns, replace=False)
        has_overflow = False
        for column in columns:
            has_overflow = has_overflow or self.game_grid_state.push_up(column, np.random.randint(0, self.game_grid_state.number_upper_bound))
        return has_overflow

    def push_garbage_rows(self, number_of_rows, number_of_columns):
        '''
        Push a garbage row to the board.
        :param number_of_rows: The number of rows to push.
        :param number_of_columns: The number of columns in the first row.
        :return: whether the board has overflowed.
        '''
        assert number_of_columns <= self.game_grid_state.column_count, 'number_of_columns must be less than or equal to column_count'
        has_overflow = False
        for row in range(number_of_rows):
            columns = np.random.permutation(self.game_grid_state.column_count)
            column_limit = 0
            if row == 0:
                column_limit = min(number_of_columns, len(columns))
            else:
                column_limit = len(columns)
            for column in columns[:column_limit]:
                has_overflow = has_overflow or self.game_grid_state.push_up(column, -2)
        return has_overflow
