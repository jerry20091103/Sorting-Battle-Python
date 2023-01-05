'''
game_base is the outermost module of the game gym.
Only this module should be imported by outside code.
'''
from sorting_battle_gym.game_board_state import GameBoardState
from sorting_battle_gym.endless_1p_game_state import Endless1PGameState
from sorting_battle_gym.endless_2p_game_state import Endless2PGameState

class GameBase:
    '''
    GameBase is the outermost class of the game gym.
    Only this class should be used by the RL agent.
    '''
    game_board_config = {
        'seed' : None,
        'row_count' : 10,
        'column_count' : 5,
        'number_upper_bound' : 10,
        'minimum_sorted_length' : 3,
        'base_remove_score' : 50,
        'remove_length_bonus' : 25,
        'max_effective_combo' : 10,
        'combo_score_step' : 2,
    }

    def __init__(self, config):
        '''
        Initialize a GameBase object.
        :param config: A dictionary containing the following
            'player_count': int
            'player_swap_delay': int , how many ticks to delay for swapping tiles
            'player_select_delay': int , how many ticks to delay for selecting tiles
            'realtime': bool, run the game in realtime (1 tick = 1/50 second)
        '''
        # init class variables
        self.player_count = config['player_count']
        self.realtime = config['realtime']
        # init a GameState object
        if self.player_count == 1:
            game_board = GameBoardState(GameBase.game_board_config)
            self.game_state = Endless1PGameState(game_board, config['player_swap_delay'],
                                                config['player_select_delay'],
                                                config['player_add_new_row_delay'])
        elif self.player_count == 2:
            p1_game_board = GameBoardState(GameBase.game_board_config)
            p2_game_board = GameBoardState(GameBase.game_board_config)
            self.game_state = Endless2PGameState(p1_game_board, p2_game_board, config['player_swap_delay'], config['player_select_delay'], config['player_add_new_row_delay'])
        else:
            raise ValueError('player_count must be 1 or 2')

    def run_game(self):
        '''
        Run the game.
        '''
        assert self.game_state.check_player_callback(), "player callback(s) are not set"
        self.game_state.run_game(self.realtime)

    def set_callback(self, callback, player_id=1):
        '''
        sets the callback function to be called when the player can take action
        :param callback: the callback function
                         (refer to the README for the callback function signature)
        :param player_id: the player id (1 or 2)
        '''
        self.game_state.set_player_callback(callback, player_id)
    