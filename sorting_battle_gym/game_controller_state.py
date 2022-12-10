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
        self.game_grid_state = game_grid_state
        self.game_score_state = game_score_state
        self.minimum_sorted_length = minimum_sorted_length
        self.selector = SelectHandler(self.game_grid_state, self.minimum_sorted_length)
        self.swapper = SwapHandler(self.game_grid_state)

    def select(self, coords):
        '''
        Call SelectHandler to select the tiles at coords, then send result to GameScoreState.
        :param coords: a list of coords.
        :return: tuple(remove number tiles count, remove garbage tiles count)
        '''
        remove_number_tiles_count, remove_garbage_tiles_count = self.selector.select(coords)
        self.game_score_state.on_remove(remove_number_tiles_count)
        return (remove_number_tiles_count, remove_garbage_tiles_count)

    def swap(self, coords):
        '''
        Call SwapHandler to swap the tiles at coord1 and coord2, then send result to GameScoreState.
        :param coord1: the first coord.
        :param coord2: the second coord.
        :return: True if swap is successful, False otherwise.
        '''
        return self.swapper.swap(coords)
