'''
This module contains the inherited game state for the endless 1p mode
'''
from sorting_battle_gym.game_state import GameState

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
        player_add_new_row_delay,
        empty_row_percentage=0.8,
        ):
        '''
        Constructor with config.
        '''
        # call base class constructor
        super().__init__(player_swap_delay, player_select_delay, player_add_new_row_delay)
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
            self.push_task(0, self.game_over_task)

    def push_one_row_task(self, player_id):
        '''
        Push one row to the game board
        '''
        assert player_id == 1, "only player 1 is supported"
        overflow = self.game_board_state.push_new_row(
            self.game_board_state.game_grid_state.column_count - 1
        )
        if overflow:
            self.game_over = True
            # give the player one last callback to notify the game is over
            self.game_end()
            # schedule the last task
            self.push_task(0, self.game_over_task)

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
        grid_2d_list = self.game_board_state.game_grid_state.get_grid()
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
        self.handle_player_action(self, 1, action_type, action_data)

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
        self.push_task(1, self.player_callback_task, 1)

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
