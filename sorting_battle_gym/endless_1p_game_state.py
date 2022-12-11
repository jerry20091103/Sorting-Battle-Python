'''
This module contains the inherited game state for the endless 1p mode
'''
from sorting_battle_gym.game_state import GameState
from sorting_battle_gym.game_state import Coord

class Endless1PGameState(GameState):
    '''
    This class implements the concrete game state for the endless 1p mode.
    It inherits the abstract base class GameState.
    '''
    def __init__(
        self,
        game_board_state,
        player_swap_delay,
        player_select_delay,
        empty_row_percentage=0.8,
        ):
        '''
        Constructor with config.
        '''
        # call base class constructor
        super().__init__(player_swap_delay, player_select_delay)
        # init game specific parameters
        self.game_board_state = game_board_state
        self.empty_row_percentage = empty_row_percentage
        self.player_callback = None
        self.init_tasks()

    def push_new_row_task(self):
        '''
        Add a new row to the game board
        '''
        overflow = self.game_board_state.push_new_row(
            self.game_board_state.game_grid_state.column_count - 1
        )
        if not overflow:
            self.push_task(self.get_tick_between_new_row(), self.push_new_row_task)
        else:
            self.game_over = True
            # give the player one last callback to notify the game is over
            self.game_end()
            # schedule the last task
            self.push_task(0, self.gamer_over_task)

    def check_player_callback(self):
        '''
        Check if the player callback is set.
        '''
        return self.player_callback is not None

    def set_player_callback(self, callback, player_id=1):
        '''
        Set the player callback.
        '''
        assert player_id == 1, "only player 1 is supported"
        self.player_callback = callback

    def player_callback_task(self, player_id):
        '''
        handles the player callback.
        '''
        assert player_id == 1, "only player 1 is supported"
        # convert the grid
        # todo : this is a bit ugly. Maybe implement get_gird() in GameGirdState?
        game_grid = self.game_board_state.game_grid_state.grid
        grid_2d_list = [[tile.val for tile in row] for row in game_grid]
        # call the player callback
        action_type, action_data = self.player_callback({
            "game_end": self.game_over,
            "level": self.level,
            "grid": grid_2d_list,
            "score": self.game_board_state.game_score_state.total_score
        })
        if self.game_over:
            return
        # handle the action
        try:
            action_delay = 0
            if action_type == 0: # idle
                action_delay = action_data
            elif action_type == 1: # swap
                assert len(action_data) == 2, "action_data must contain 2 coordinates when swapping"
                coord1 = Coord(action_data[0][0], action_data[0][1])
                coord2 = Coord(action_data[1][0], action_data[1][1])
                assert self.game_board_state.game_controller_state.swap([coord1, coord2]), "invalid swap"
                action_delay = self.player_swap_delay
                # todo: get the swap is valid or not for the player?
            elif action_type == 2: # select
                assert action_data is not None, "action_data must not be None when selecting"
                (tile_number, garbage_number) = self.game_board_state.game_controller_state.select(action_data)
                action_delay = self.player_select_delay
                assert tile_number > 0, "invalid select"
            # schedule the next callback
            self.push_task(action_delay, self.player_callback_task, player_id)
        except AssertionError as e:
            # pause the game and show the error message
            print("[ERROR] in player_callback_task:", e)
            # print action type and data
            print("action_type:", action_type, ", action_data:", action_data)
            input("The previous callback wiil be sent again. Press any key to continue...")
            self.push_task(0, self.player_callback_task, player_id)

    def init_tasks(self):
        '''
        Add required initial tasks when the game starts.
        Must call super().init_tasks() first.
        '''
        # call base class init tasks
        super().init_tasks()
        # load the initial grid
        self.push_task(0, self.load_task)
        # schedule first player callback
        self.push_task(0, self.player_callback_task, 1)

    def game_end(self):
        '''
        notify the player that the game is over
        '''
        self.push_task(0, self.player_callback_task, 1)

    def load_task(self):
        '''
        Load the initial grid with random tiles.
        '''
        self.game_board_state.game_grid_state.load_random(self.empty_row_percentage)
