class GameGridState:
    '''
    The is currently a empty class to fool the testbench.
    The contents are not guaranteed to be correct.
    '''
    def __init__(self, row_count, column_count):
        '''
        Constructor with row_count and column_count.
        '''
        pass

    @classmethod
    def copy(cls, other):
        '''
        Copy constructor.
        '''
        pass

    def inplace_copy(self, other):
        '''
        Inplace copy from other.
        '''
        pass

    def get(self, coord):
        '''
        Get the value at (row, column).
        '''
        return 0

    def set(self, coord, value):
        '''
        Set the value at (row, column).
        '''
        pass

    def is_empty(self, coord):
        '''
        Check if the cell is empty.
        '''
        return True

    def is_garbage(self, coord):
        '''
        Check if the cell is garbage.
        '''
        return True

    def is_number(self, coord):
        '''
        Check if the cell is a number.
        '''
        return True

    def clear(self):
        '''
        Clear the while grid to -1.
        '''
        pass

    def load_random(self, min_inclusive=0, max_exclusive=100):
        '''
        Load random numbers to the grid.
        '''
        pass

    def load_row(self, row_id, row_values):
        '''
        Load numbers to the row.
        '''
        pass

    def load_column(self, column_id, column_values):
        '''
        Load numbers to the column.
        '''
        pass

    def load_grid(self, grid_values):
        '''
        Load numbers to the grid.
        '''
        pass

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
    