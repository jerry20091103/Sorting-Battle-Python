'''
This module generates action table.
'''
dir = [[0, 1], [0, -1], [1, 0], [-1, 0]]
table = []
SWAP = 1
SELECT = 2
ADD_NEW_LINE = 3

NUM_SWAP = 0
for i in range(50):
    row = i // 5
    col = i % 5
    for (dr, dc) in dir:
        nr = row + dr
        nc = col + dc

        if (nr >= 10 or nc >= 5):
            continue
        if (nc < 0 or nr < 0):
            continue

        NUM_SWAP += 1
        table.append([ SWAP, [[row, col], [nr, nc]] ])
print(f"Total number of swap: {NUM_SWAP}")

NUM_SELECT = 0
for i in range(50):
    row = i // 5
    col = i % 5
    for (dr, dc) in dir:
        # len 9 is OK but too dangerous
        for LEN in range(2, 9):
            nr = row + dr * LEN
            nc = col + dc * LEN

            if (nr >= 10 or nc >= 5):
                continue
            if (nc < 0 or nr < 0):
                continue

            NUM_SELECT += 1
            tmp = [[row, col]]
            for j in range(LEN):
                tmp.append([tmp[-1][0] + dr, tmp[-1][1] + dc])
            table.append([ SELECT, tmp ])
print(f"Total number of select: {NUM_SELECT}")

# 1 is for add new blocks
table.append([ ADD_NEW_LINE, None ])
print(f"Number of actions: {NUM_SWAP + NUM_SELECT + 1}\n")

TOTAL_NUM = NUM_SWAP + NUM_SELECT + 1
print("==============================")
print("action id|action type|action data")
for i in range(TOTAL_NUM):
    print(f"|{i:8}|{table[i][0]:^11}|{table[i][1]}")
