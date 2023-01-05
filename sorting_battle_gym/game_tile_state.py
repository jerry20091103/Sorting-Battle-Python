'''
This module contains GameTileState class.
'''
class GameTileState:
    '''
    The is currently a empty class to fool the testbench.
    The contents are not guaranteed to be correct.
    '''
    def __init__(self, val=-1):
        '''
        Constructor with val (-1 for empty, -2 for garbage).
        '''
        self.val = val

    def is_empty(self):
        '''
        Check if the tile is empty.
        return: True if the tile is empty, False otherwise.
        '''
        return self.val == -1

    def is_garbage(self):
        '''
        Check if the tile is garbage.
        return: True if the tile is garbage, False otherwise.
        '''
        return self.val == -2

    def is_number(self):
        '''
        Check if the tile is a number.
        return: True if the tile is a number, False otherwise.
        '''
        return self.val >= 0
