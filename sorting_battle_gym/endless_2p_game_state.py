'''
This module contains the Endless2PGameState class, which is a child of VersusGameState
'''
import numpy as np
from sorting_battle_gym.versus_game_state import VersusGameState
from sorting_battle_gym.game_state import Coord

class Endless2PGameState(VersusGameState):
    '''
    This class implements the concrete game state for the endless 2p mode.
    '''
    def __init__(
        self,
        p1_game_board_state,
        p2_game_board_state,
        player_swap_delay,
        player_select_delay,
        ):
        '''
        Constructor with config.
        '''
        # call base class constructor
        super().__init__(player_swap_delay, player_select_delay)
        self.init_tasks()
        self.register_player(p1_game_board_state)
        self.register_player(p2_game_board_state)

    def get_tick_between_new_row(self):
        '''
        Row appears less frequently in 2P mode.
        '''
        return int(round(300 - 200 * np.clip(np.power(self.level/20, 4), 0, 1)))

    def on_draw(self):
        '''
        Inherited from the base class.
        Nothing to do for now
        '''

    def player_callback_task(self, player_id):
        '''
        The callback task for the player
        :param player_id: the player id (starts from 1)
        '''
        assert 0 < player_id <= 2, "player id needs to be 1 or 2"
        current_player = self.player_states[player_id - 1]
        oppoent_id = 1 if player_id == 2 else 2
        opponent_player = self.player_states[oppoent_id - 1]
        # call the player callback
        action_type, action_data = self.player_states[player_id - 1].player_callback({
            'game_end': self.game_over,
            'level': self.level,
            'grid': current_player.game_board_state.game_grid_state.get_grid(),
            'score': current_player.game_board_state.game_score_state.total_score,
            'opponent_grid': opponent_player.game_board_state.game_grid_state.get_grid(),
            'opponent_score': opponent_player.game_board_state.game_score_state.total_score,
        })
        if self.game_over:
            return
        # handle the action
        self.handle_player_action(current_player, player_id, action_type, action_data)
