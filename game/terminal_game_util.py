'''
This module contains common utility functions for the terminal game.
'''

def get_tile_char(tile_val):
    '''
    Get the character representation of the tile value.
    :param tile_val: the tile value.
    :return: the character representation of the tile value.
    '''
    if tile_val == -1:
        return "   "
    if tile_val == -2:
        return "  X"
    return "  "+ str(tile_val)

def show_game_status(add_tab, game_end, level, score, grid, pressure=None):
    '''
    print out the game status in terminal for one player.
    '''
    tabs = '\t\t\t\t\t' if add_tab else ''
    # show level and score
    print (tabs, "=========================")
    print(tabs, "Game End: ", game_end)
    print(tabs, "Level: ", level, " Score: ", score)
    # show pressure
    if pressure is not None:
        print(tabs, "Pressure: ", pressure)
    # show grid as well as row and column index
    print(tabs, "    ", end="")
    for i in range(len(grid[0])):
        print(f"{i:3}", end="")
    print()
    print(tabs, "    " + "-" * (len(grid[0]) * 3))
    for i in range(len(grid)):
        print(tabs, f"{i:3}", end="|")
        for tile in grid[i]:
            print(f"{get_tile_char(tile):3}", end="")
        print()

def get_action_from_terminal():
    '''
    Get the action from terminal.
    :return: the action type and the action parameters.
    '''
    try:
        action_type = int(input("Enter action type (idle:0, swap:1, select:2): "))
        # idle
        if action_type == 0:
            # get delay ticks
            delay_ticks = int(input("Enter delay in ticks: "))
            return action_type, delay_ticks
        # swap
        if action_type == 1:
            coord_list = []
            # get 2 coordinates
            for i in range(2):
                coord_x, coord_y = input(f"Enter coord {i} (x y): ").split()
                coord_list.append((int(coord_x), int(coord_y)))
            return action_type, coord_list
        # select
        if action_type == 2:
            coord_list = []
            # input a list of coordinates
            coord = input("Enter coord (f when done) (x y): ")
            while coord != "f":
                coord_x, coord_y = coord.split()
                coord_list.append((int(coord_x), int(coord_y)))
                coord = input("Enter coord (f when done) (x y): ")
            return action_type, coord_list
    # catch int conversion error
    except ValueError:
        print("[ERROR] Invalid input, int() conversion error")
        return None, None
    print("[ERROR] Invalid action type")
    return None, None
