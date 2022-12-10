from sorting_battle_gym.game_grid_state import GameGridState
from sorting_battle_gym.game_score_state import GameScoreState
from sorting_battle_gym.select_handler import SelectHandler
from sorting_battle_gym.swap_handler import SwapHandler

class GameControllerState:
    '''
    GameControllerState represents a player's inputs to the board.
    Has public methods that represent the actions a player (or agent) can take, like selecting and swapping.
    '''

    def __init__(self, game_grid_state, game_score_state, minimum_sorted_length=3):
        '''
        Constructor with game_grid_state, game_score_state, and minimum_sorted_length.
        :param game_grid_state: the GameGridState object.
        :param game_score_state: the GameScoreState object.
        :param minimum_sorted_length: the minimum length of sorted sequence.
        '''
        pass

    def select(self, coords):
        '''
        Call SelectHandler to select the tiles at coords, then send result to GameScoreState.
        :param coords: a list of coords.
        :return: tuple(remove number tiles count, remove garbage tiles count)
        '''
        # TODO: call SelectHandler to select the tiles at coords
        # TODO: send result to GameScoreState by on_remove()
        pass
        # question1: call on_remove() with parameter send remove_numve_tiles_count? (no need for garbage)
        # question2: need to call on_remove() even if remove_number_tiles_count <3? (for combo purpose)

    def swap(self, coord1, coord2):
        '''
        Call SwapHandler to swap the tiles at coord1 and coord2, then send result to GameScoreState.
        :param coord1: the first coord.
        :param coord2: the second coord.
        :return: True if swap is successful, False otherwise.
        '''
        # TODO: call SwapHandler to swap the tiles at coord1 and coord2
        # TODO: send result to GameScoreState by on_swap()
        pass
        # question1: still need to send result to GameScoreState? (for combo purpose)
