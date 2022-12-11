'''
This is a interactive terminal version of the 1P game for testing.
Also serves as an example of how to use the gym
'''
# add include path
import sys
sys.path.append("../")
from sorting_battle_gym.game_base import GameBase

def player1_callback(game_end, level, grid1, score1, grid2=None, score2=None):
    # show level and score
    print ("=========================")
    print("Game End: ", game_end)
    print("Level: ", level, " Score: ", score1)
    # show grid as well as row and column index
    print("    ", end="")
    for i in range(len(grid1[0])):
        print(f"{i:3}", end="")
    print()
    print("    " + "-" * (len(grid1[0]) * 3))
    for i in range(len(grid1)):
        print(f"{i:3}", end="|")
        for tile in grid1[i]:
            print(f"{tile:3}", end="")
        print()
    # get action
    action_type = int(input("Enter action type (idle:0, swap:1, select:2): "))
    # idle
    if action_type == 0:
        # get delay ticks
        delay_ticks = int(input("Enter delay in ticks: "))
        return action_type, delay_ticks
    # swap
    elif action_type == 1:
        coord_list = []
        # get 2 coordinates
        for i in range(2):
            coord_x, coord_y = input(f"Enter coord {i} (x y): ").split()
            coord_list.append([int(coord_x), int(coord_y)])
        return action_type, coord_list
    # select
    elif action_type == 2:
        coord_list = []
        # input a list of coordinates
        coord = input("Enter coord (f when done) (x y): ")
        while coord != "f":
            coord_x, coord_y = coord.split()
            coord_list.append([int(coord_x), int(coord_y)])
            coord = input("Enter coord (f when done) (x y): ")
        return action_type, coord_list

config = {
    'player_count': 1,
    'player_swap_delay': 10,
    'player_select_delay': 50,
    'realtime': False
}
game_base = GameBase(config)
game_base.set_callback(player1_callback, 1)
game_base.run_game()