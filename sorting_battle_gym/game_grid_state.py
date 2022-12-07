import random
from game_tile_state import GameTileState

class GameGridState:
    '''
    The is currently a empty class to fool the testbench.
    The contents are not guaranteed to be correct.
    '''
    def __init__(self, row_count, column_count):
        '''
        Constructor with row_count and column_count.
        :param row_count: the number of rows.
        :param column_count: the number of columns.
        '''
        self.row_count = row_count
        self.column_count = column_count
        self.grid = [[GameTileState() for _ in range(column_count)] for _ in range(row_count)]

    @classmethod
    def copy(cls, other):
        '''
        Copy constructor.
        :param other: the other GameGridState object to copy.
        :return: the copied GameGridState object.
        '''
        copy_state = cls(other.row_count, other.column_count)
        copy_state.inplace_copy(other)
        return copy_state

    def inplace_copy(self, other):
        '''
        Inplace copy from other.
        :param other: the other GameGridState object to copy.
        '''
        for row in range(self.row_count):
            for column in range(self.column_count):
                self.grid[row][column].val = other.grid[row][column].val

    def get(self, coord):
        '''
        Get the value at (row, column).
        :param coord: tuple(row, column).
        :return: the value at (row, column).
        '''
        # the coord should be check for out of bound
        return self.grid[coord[0]][coord[1]].val

    def set(self, coord, value):
        '''
        Set the value at (row, column).
        :param coord: tuple(row, column).
        :param value: the value to set.
        '''
        # the coord should be check for out of bound
        self.grid[coord[0]][coord[1]].val = value

    def is_empty(self, coord):
        '''
        Check if the cell is empty.
        :param coord: tuple(row, column).
        :return: True if the cell is empty, False otherwise.
        '''
        return self.grid[coord[0]][coord[1]].is_empty()

    def is_garbage(self, coord):
        '''
        Check if the cell is garbage.
        :param coord: tuple(row, column).
        :return: True if the cell is garbage, False otherwise.
        '''
        return self.grid[coord[0]][coord[1]].is_garbage()

    def is_number(self, coord):
        '''
        Check if the cell is a number.
        :param coord: tuple(row, column).
        :return: True if the cell is a number, False otherwise.
        '''
        return self.grid[coord[0]][coord[1]].is_number()

    def clear(self):
        '''
        Clear the while grid to -1.
        '''
        for row in range(self.row_count):
            for column in range(self.column_count):
                self.grid[row][column].val = -1

    def load_random(self, min_inclusive=0, max_exclusive=100):
        '''
        Load random numbers to the grid.
        :param min_inclusive: the minimum number to generate.
        :param max_exclusive: the maximum number to generate plus one.
        '''
        for row in range(self.row_count):
            for column in range(self.column_count):
                self.grid[row][column].val = random.randrange(min_inclusive, max_exclusive)

    def load_row(self, row_id, row_values):
        '''
        Load numbers to the row.
        :param row_id: the row index.
        :param row_values: the list of numbers to load.
        '''
        # the row_id should be check for out of bound
        # the row_values should be check for length
        for column in range(self.column_count):
            self.grid[row_id][column].val = row_values[column]

    def load_column(self, column_id, column_values):
        '''
        Load numbers to the column.
        :param column_id: the column index.
        :param column_values: the list of numbers to load.
        '''
        # the column_id should be check for out of bound
        # the column_values should be check for length
        for row in range(self.row_count):
            self.grid[row][column_id].val = column_values[row]

    def load_grid(self, grid_values):
        '''
        Load numbers to the grid.
        :param grid_values: the list of list of numbers to load.
        '''
        # the grid_values should be check for length
        for row in range(self.row_count):
            for column in range(self.column_count):
                self.grid[row][column].val = grid_values[row][column]

    def pull_down(self, column):
        '''
        Pull down the column.
        '''
        pass

    def swap(self, coord1, coord2):
        '''
        Swap the value of two tiles.
        '''
        pass

    def swap_and_pull_down(self, coord1, coord2):
        '''
        Swap the value of two tiles and pull down.
        '''
        pass

    def push_up(self, column, number):
        '''
        Push up the column with number.
        Returns whether the column has overflowed.
        '''
        return False

    def remove_tiles(self, tiles):
        '''
        Remove the tiles from the grid.
        '''
        pass

    def content_equal(self, other):
        '''
        Check if the content of two grids are equal.
        '''
        return True
    