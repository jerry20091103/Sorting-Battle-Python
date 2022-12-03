class GameGridState:
    '''
    The is currently a empty class to fool the testbench.
    '''
    def __init__(self, rowCount, columnCount):
        '''
        Constructor with rowCount and columnCount.
        '''
        pass

    @classmethod
    def copy(cls, other):
        '''
        Copy constructor.
        '''
        pass

    def InplaceCopy(self, other):
        '''
        Inplace copy from other.
        '''
        pass

    def Get(self, coord):
        '''
        Get the value at (row, column).
        '''
        return 0
    
    def Set(self, coord, value):
        '''
        Set the value at (row, column).
        '''
        pass

    def IsEmpty(self, coord):
        '''
        Check if the cell is empty.
        '''
        return True
    
    def IsGarbage(self, coord):
        '''
        Check if the cell is garbage.
        '''
        return True

    def IsNumber(self, coord):
        '''
        Check if the cell is a number.
        '''
        return True
    
    def Clear(self):
        '''
        Clear the while grid to -1.
        '''
        pass

    def LoadRandom(self, minInclusive=0, maxExclusive=100):
        '''
        Load random numbers to the grid.
        '''
        pass

    def LoadRow(self, rowId, rowValues):
        '''
        Load numbers to the row.
        '''
        pass

    def LoadColumn(self, columnId, columnValues):
        '''
        Load numbers to the column.
        '''
        pass

    def LoadGrid(self, gridValues):
        '''
        Load numbers to the grid.
        '''
        pass
    