from sorting_battle_gym.game_state import GameState
from sorting_battle_gym.game_board_state import GameBoardState

class VersusGameState(GameState):
    '''
    Abstract base classes for game modes that have more than 1 player.
    It inherits the abstract base class GameState.
    '''
    class PlayerState:
        '''
        This class represents a player in VersusGameState.
        '''
        # todo ...
        # * class constants does not need "self."
    
    def __init__(self, player_swap_delay, player_select_delay):
        '''
        class constructor
        This base class constructor should be called by the derived class constructor
        '''
        # must call base class constructor
        super().__init__(player_swap_delay, player_select_delay)
        # class variables
        self.player_states = []
        # todo ...