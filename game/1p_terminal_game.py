'''
This is a interactive terminal version of the 1P game for testing.
Also serves as an example of how to use the gym
'''
# add include path
import sys
from sorting_battle_gym.game_base import GameBase
sys.path.append("../")

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

def player1_callback(game_status):
    '''
    Callback to control the player 1 from terminal.
    '''
    # show level and score
    print ("=========================")
    print("Game End: ", game_status["game_end"])
    print("Level: ", game_status["level"], " Score: ", game_status["score"])
    grid1 = game_status["grid"]
    # show grid as well as row and column index
    print("    ", end="")
    for i in range(len(grid1[0])):
        print(f"{i:3}", end="")
    print()
    print("    " + "-" * (len(grid1[0]) * 3))
    for i in range(len(grid1)):
        print(f"{i:3}", end="|")
        for tile in grid1[i]:
            print(f"{get_tile_char(tile):3}", end="")
        print()
    # get action
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

config = {
    'player_count': 1,
    'player_swap_delay': 10,
    'player_select_delay': 50,
    'realtime': False
}
game_base = GameBase(config)
game_base.set_callback(player1_callback, 1)
game_base.run_game()
