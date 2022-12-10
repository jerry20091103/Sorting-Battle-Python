class SelectHandler:
    '''
    SelectHandler handles the select command of player or agent.
    '''

    def __init__(self, game_grid_state, minimum_sorted_length=3):
        '''
        Constructor with game_grid_state and minimum_sorted_length.
        :param game_grid_state: the GameGridState object.
        :param minimum_sorted_length: the minimum length of sorted sequence.
        '''
        self.game_grid_state = game_grid_state
        self.minimum_sorted_length = minimum_sorted_length
        
    def select(self, coords):
        '''
        This method should check valid, and call functions in gameGridState to remove tiles.
        :param coords: a list of coords.
        :return: tuple(remove number tiles count, remove garbage tiles count)
        '''
        # check command is valid
        if (self.check_valid(coords) == False):
            return (0, 0)
        number_tiles_count = len(coords)

        # search for the garbage tiles that should be removed
        garbage_tiles = self.search_garbage_tiles(coords)
        garbage_tiles_count = len(garbage_tiles)

        # remove the tiles and pull down columns using game_grid_state
        tiles_to_remove = []
        print(tiles_to_remove)
        tiles_to_remove = coords
        print(tiles_to_remove)
        tiles_to_remove.extend(garbage_tiles)
        print(tiles_to_remove)
        self.game_grid_state.remove_tiles(tiles_to_remove)
        
        return (number_tiles_count, garbage_tiles_count)

    def check_valid(self, coords):
        '''
        This method should check valid.
        :param coords: a list of coords.
        :return: True if valid, False otherwise.
        '''
        # short selection
        if len(coords) < self.minimum_sorted_length:
            return False
        
        # coords[0] first
        # check is in board
        if coords[0][0] < 0 or coords[0][0] >= self.game_grid_state.row_count or coords[0][1] < 0 or coords[0][1] >= self.game_grid_state.column_count:
            return False
        # check is number
        if not self.game_grid_state.is_number(coords[0]):
            return False

        # set and check direction
        direction = (coords[1][0] - coords[0][0], coords[1][1] - coords[0][1])
        if abs(direction[0]) + abs(direction[1]) != 1:
            return False

        is_increasing = self.game_grid_state.get(coords[-1]) > self.game_grid_state.get(coords[0])

        # other coords
        for i in range(1, len(coords)):
            # check is in board
            if coords[i][0] < 0 or coords[i][0] >= self.game_grid_state.row_count or coords[i][1] < 0 or coords[i][1] >= self.game_grid_state.column_count:
                return False
            # check is number
            if not self.game_grid_state.is_number(coords[i]):
                return False
            # check is adjacent and in a line
            if coords[i-1][0]+direction[0] != coords[i][0] or coords[i-1][1]+direction[1] != coords[i][1]:
                return False
            # check is sorted
            if is_increasing:
                if self.game_grid_state.get(coords[i]) < self.game_grid_state.get(coords[i-1]):
                    return False
            else:
                if self.game_grid_state.get(coords[i]) > self.game_grid_state.get(coords[i-1]):
                    return False

        return True

    def search_garbage_tiles(self, coords):
        '''
        This method should search and return garbage tiles.
        :param coords: a list of coords.
        :return: the list of garbage tiles that should be removed.
        '''
        vertical = (coords[1][0] - coords[0][0]) != 0
        garbage_tiles = []
        coords.sort()
        if vertical:
            # remove garbage on the top
            temp_coord = (coords[0][0] - 1, coords[0][1])
            if (temp_coord[0] >= 0 and self.game_grid_state.is_garbage(temp_coord)):
                garbage_tiles.append(temp_coord)
            # remove garbage on the bottom
            temp_coord = (coords[-1][0] + 1, coords[-1][1])
            if (temp_coord[0] < self.game_grid_state.row_count and self.game_grid_state.is_garbage(temp_coord)):
                garbage_tiles.append(temp_coord)
            # remove garbage on the left
            if (coords[0][1] - 1 >= 0):
                for coord in coords:
                    temp_coord = (coord[0], coord[1] - 1)
                    if self.game_grid_state.is_garbage(temp_coord):
                        garbage_tiles.append(temp_coord)
            # remove garbage on the right
            if (coords[0][1] + 1 < self.game_grid_state.column_count):
                for coord in coords:
                    temp_coord = (coord[0], coord[1] + 1)
                    if self.game_grid_state.is_garbage(temp_coord):
                        garbage_tiles.append(temp_coord)
        else:
            # remove garbage on the left
            temp_coord = (coords[0][0], coords[0][1] - 1)
            if (temp_coord[1] >= 0 and self.game_grid_state.is_garbage(temp_coord)):
                garbage_tiles.append(temp_coord)
            # remove garbage on the right
            temp_coord = (coords[-1][0], coords[-1][1] + 1)
            if (temp_coord[1] < self.game_grid_state.column_count and self.game_grid_state.is_garbage(temp_coord)):
                garbage_tiles.append(temp_coord)
            # remove garbage on the top
            if (coords[0][0] - 1 >= 0):
                for coord in coords:
                    temp_coord = (coord[0] - 1, coord[1])
                    if self.game_grid_state.is_garbage(temp_coord):
                        garbage_tiles.append(temp_coord)
            # remove garbage on the bottom
            if (coords[0][0] + 1 < self.game_grid_state.row_count):
                for coord in coords:
                    temp_coord = (coord[0] + 1, coord[1])
                    if self.game_grid_state.is_garbage(temp_coord):
                        garbage_tiles.append(temp_coord)

        return garbage_tiles