class SwapHandler:
    '''
    SwapHandler handles the swap command of player or agent.
    '''
    def __init__(self, game_grid_state):
        '''
        Constructor with game_grid_state.
        :param game_grid_state: the GameGridState object.
        '''
        self.game_grid_state = game_grid_state

    def swap(self, coords):
        '''
        This method should check valid, and call functions in gameGridState to swap tiles.
        :param coord1: the first coord.
        :param coord2: the second coord.
        :return: True if swap is successful, False otherwise.
        '''
        coord1 = coords[0]
        coord2 = coords[1]
        # check command is valid
        if not self.check_valid(coord1, coord2):
            return False
        # swap the tiles using game_grid_state
        self.game_grid_state.swap_and_pull_down(coord1, coord2)
        return True

    def check_valid(self, coord1, coord2):
        '''
        This method should check valid.
        :param coord1: the first coord.
        :param coord2: the second coord.
        :return: True if valid, False otherwise.
        '''
        # check is in board
        if (coord1[0] < 0 or coord1[0] >= self.game_grid_state.row_count or \
            coord1[1] < 0 or coord1[1] >= self.game_grid_state.column_count):
            return False
        if (coord2[0] < 0 or coord2[0] >= self.game_grid_state.row_count or \
            coord2[1] < 0 or coord2[1] >= self.game_grid_state.column_count):
            return False

        # check is adjacent
        if abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1]) != 1:
            return False

        # check is number
        if not self.game_grid_state.is_number(coord1):
            return False
        if not self.game_grid_state.is_number(coord2):
            return False

        return True
