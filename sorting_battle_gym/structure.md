## GameBoardState
### var
- dict config {
    - int seed
    - int rowCount, columnCount
    - int minimumSortedLength
    - int baseRemoveScore
    - int maxEffectiveCombo
    - float comboScoreStep
}
- GameGridState gameGridState
- np.randomInstance
- GameControllerState gameControllerState
- GameScoreState gameScoreState
### method
- GameBoardState(dict config)

## GameTileState
### const
- Empty = -1
- Garbage = -2
### var
- number
### method
- GameTileState(int val = Empty)
- IsEmpty()
- IsGarbage()
- IsNumber()

## GameGridState
### var
- rowCount
- columnCount
- grid
    - 2D-list of GameTileState
### method
- GameGridState(int rowCount, int columnCount) # initialize to -1 (Empty)
- copy(other) # copy constructor (classmethod!)
- void InplaceCopy(GameGridState other)
- int Get(tuple coord)
- void Set(tuple coord, int value)
- bool IsEmpty(tuple coord)
- bool IsGarbage(tuple coord)
- bool IsNumber(tuple coord)
- void Clear() # flush to -1
- void LoadRandom(int minInclusive, int maxExclusive)
- void LoadRow(int rowId, list rowValues)
- void LoadColumn(int columnId, list columnValues)
- void LoadGrid(list gridValues) # gridValues is a 2D-list
- void PullDown(int column)
- void Swap(tuple coord1, tuple coord2)
- void SwapAndPullDown()
- void PushUp()
- void RemoveTiles(list[tuple] coords)
- bool ContentEqual(GameGridState other)

## GameControllerState
### var
- GameGridState gameGridState (from gameBoardState)
- GameScoreState gameScoreState (from gameBoardState)
- int minimumSortedLength
- SelectHandler selecter
- SwapHandler swaper
### method
- GameControllerState(GameGridState gameGridState, GameScoreState gameScoreState, int minimumSortedLength)
- int Select(list[tuple]) # call selector, and send result to gameScoreState
- bool Swap(list[tuple])

## SelectHandler
## SwapHandler

## GameScoreState
### var
- int totalScore
- int combo
- int comboScoreBuffer
- dict config {
    int minimumRemoveCount, baseRemoveScore, maxEffectiveCombo, RemoveLengthBonus
    float comboScoreStep
}
### method
- GameScoreState(dict config)
- void OnRemove(int removeCount)
