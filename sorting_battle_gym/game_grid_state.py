'''
This module contains the inherited game state for the endless 1p mode
'''
import random
from math import floor
from sorting_battle_gym.game_tile_state import GameTileState

class GameGridState:
    '''
    GameGridState represents a grid.
    Exposes some public methods for manipulating the grid.
    A board only has one grid.
    '''
    def __init__(self, row_count, column_count, number_upper_bound=10):
        '''
        Constructor with row_count and column_count.
        :param row_count: the number of rows.
        :param column_count: the number of columns.
        '''
        self.row_count = row_count
        self.column_count = column_count
        self.number_upper_bound = number_upper_bound
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
        assert coord[0] >= 0 and coord[0] < self.row_count and \
               coord[1] >= 0 and coord[1] < self.column_count
        return self.grid[coord[0]][coord[1]].val

    def set(self, coord, value):
        '''
        Set the value at (row, column).
        :param coord: tuple(row, column).
        :param value: the value to set.
        '''
        assert coord[0] >= 0 and coord[0] < self.row_count and \
               coord[1] >= 0 and coord[1] < self.column_count
        self.grid[coord[0]][coord[1]].val = value

    def is_empty(self, coord):
        '''
        Check if the cell is empty.
        :param coord: tuple(row, column).
        :return: True if the cell is empty, False otherwise.
        '''
        assert coord[0] >= 0 and coord[0] < self.row_count and \
               coord[1] >= 0 and coord[1] < self.column_count
        return self.grid[coord[0]][coord[1]].is_empty()

    def is_garbage(self, coord):
        '''
        Check if the cell is garbage.
        :param coord: tuple(row, column).
        :return: True if the cell is garbage, False otherwise.
        '''
        assert coord[0] >= 0 and coord[0] < self.row_count and \
               coord[1] >= 0 and coord[1] < self.column_count
        return self.grid[coord[0]][coord[1]].is_garbage()

    def is_number(self, coord):
        '''
        Check if the cell is a number.
        :param coord: tuple(row, column).
        :return: True if the cell is a number, False otherwise.
        '''
        assert coord[0] >= 0 and coord[0] < self.row_count and \
               coord[1] >= 0 and coord[1] < self.column_count
        return self.grid[coord[0]][coord[1]].is_number()

    def clear(self):
        '''
        Clear the while grid to -1.
        '''
        for row in range(self.row_count):
            for column in range(self.column_count):
                self.grid[row][column].val = -1

    def load_random(self, empty_row_percentage=1):
        '''
        Load random numbers to the grid.
        :param row_percentage: the percentage of rows that are filled with random numbers.
                               range of the numbers: [0, number_upper_bound).
        '''
        assert 0 <= empty_row_percentage <= 1
        empty_row_number = floor(self.row_count * empty_row_percentage)
        for row in range(empty_row_number, self.row_count):
            for column in range(self.column_count):
                self.grid[row][column].val = random.randrange(0, self.number_upper_bound)

    def load_row(self, row_id, row_values):
        '''
        Load numbers to the row.
        :param row_id: the row index.
        :param row_values: the list of numbers to load.
        '''
        assert 0 <= row_id < self.row_count
        assert len(row_values) == self.column_count
        for column in range(self.column_count):
            self.grid[row_id][column].val = row_values[column]

    def load_column(self, column_id, column_values):
        '''
        Load numbers to the column.
        :param column_id: the column index.
        :param column_values: the list of numbers to load.
        '''
        assert 0 <= column_id < self.column_count
        assert len(column_values) == self.row_count
        for row in range(self.row_count):
            self.grid[row][column_id].val = column_values[row]

    def load_grid(self, grid_values):
        '''
        Load numbers to the grid.
        :param grid_values: the list of list of numbers to load.
        '''
        assert len(grid_values) * len(grid_values[0]) == self.row_count * self.column_count
        for row in range(self.row_count):
            for column in range(self.column_count):
                self.grid[row][column].val = grid_values[row][column]

    def get_grid(self):
        '''
        Get the grid in 2D list.
        :return: the grid in 2D list.
        '''
        return [[tile.val for tile in row] for row in self.grid]

    def pull_down(self, column):
        '''
        Pull down the column.
        :param column: the column index.
        '''
        assert 0 <= column < self.column_count

        row_to_fill = self.row_count - 1
        while row_to_fill >= 0 and (not self.grid[row_to_fill][column].is_empty()):
            row_to_fill -= 1
        row_to_pull = row_to_fill - 1
        while row_to_pull >= 0 and row_to_fill >= 0:
            if self.grid[row_to_pull][column].is_empty():
                row_to_pull -= 1
            else:
                self.grid[row_to_fill][column].val = self.grid[row_to_pull][column].val
                self.grid[row_to_pull][column].val = -1
                row_to_pull -= 1
                row_to_fill -= 1

    def swap(self, coord1, coord2):
        '''
        Swap the value of two tiles.
        :param coord1: tuple(row, column) of the first tile.
        :param coord2: tuple(row, column) of the second tile.
        '''
        assert coord1[0] >= 0 and coord1[0] < self.row_count and \
               coord1[1] >= 0 and coord1[1] < self.column_count
        assert coord2[0] >= 0 and coord2[0] < self.row_count and \
               coord2[1] >= 0 and coord2[1] < self.column_count
        if coord1[0] != coord2[0] or coord1[1] != coord2[1]:
            self.grid[coord1[0]][coord1[1]].val, self.grid[coord2[0]][coord2[1]].val = \
                self.grid[coord2[0]][coord2[1]].val, self.grid[coord1[0]][coord1[1]].val

    def swap_and_pull_down(self, coord1, coord2):
        '''
        Swap the value of two tiles and pull down.
        :param coord1: tuple(row, column) of the first tile.
        :param coord2: tuple(row, column) of the second tile.
        '''
        self.swap(coord1, coord2)
        self.pull_down(coord1[1])
        self.pull_down(coord2[1])

    def push_up(self, column, number):
        '''
        Push up the column with number.
        Returns whether the column has overflowed.
        :param column: the column index.
        :param number: the number to push up.
        :return: True if the column has overflowed, False otherwise.
        '''
        assert 0 <= column < self.column_count
        overflow = (not self.grid[0][column].is_empty())
        for row in range(self.row_count - 1):
            self.grid[row][column].val = self.grid[row + 1][column].val
        self.grid[self.row_count - 1][column].val = number
        return overflow

    def remove_tiles(self, tiles):
        '''
        Remove the tiles from the grid.
        :param tiles: the list of tiles to remove.
        '''
        for tile in tiles:
            assert tile[0] >= 0 and tile[0] < self.row_count and \
                   tile[1] >= 0 and tile[1] < self.column_count
            self.grid[tile[0]][tile[1]].val = -1
        for column in range(self.column_count):
            self.pull_down(column)

    def content_equal(self, other):
        '''
        Check if the content of two grids are equal.
        :param other: the other grid to compare.
        :return: True if the content of two grids are equal, False otherwise.
        '''
        assert self.row_count == other.row_count and \
               self.column_count == other.column_count
        for row in range(self.row_count):
            for column in range(self.column_count):
                if self.grid[row][column].val != other.grid[row][column].val:
                    return False
        return True
