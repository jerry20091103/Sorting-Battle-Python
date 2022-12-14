from sorting_battle_gym.game_state import GameState
from sorting_battle_gym.game_board_state import GameBoardState
from abc import abstractmethod

class VersusGameState(GameState):
    '''
    Abstract base classes for game modes that have more than 1 player.
    It inherits the abstract base class GameState.
    '''
    class PlayerState:
        '''
        This class represents a player in VersusGameState.
        '''
        # todo ...
        # * class constants does not need "self."

        def __init__(self, game_state, game_board_state):
            '''
            class constructor
            :param game_state: the GameState object, should be its own parent
            :param game_board_state: the GameBoardState object of the player
            '''
            pass

        def reset_pressure_tick(self):
            '''
            in unity:
            // ! This is invoked whenever the player's pressure changed.
            // ! Together with "PressureTickDuration", this makes each ReceiveTrashEvent
            // ! happen at least PressureTickDuration apart.
            '''
            pass

        def attack(self, score_increase_info):
            '''
            Attack the other player.
            This function needs to be called by GameScoreState when the score increase.
            :param score_increase_info: TBE
            '''
            pass

        def compute_attack_power(self, score_increase_info):
            '''
            Compute the attack power.
            :param score_increase_info: TBE
            :return: the attack power
            '''
            pass

        def compute_attack_load(self, garbage):
            '''
            Compute the attack load.
            :param garbage: int, TBE
            :return: (int: num_rows, int: num_columns), TBE
            '''
            pass

        def load_task(self):
            '''
            Task to load the game board with random numbers.
            '''
            pass

        def check_receive_garbage_task(self):
            '''
            Check if the player needs to receive garbage from pressure?
            '''
            pass
    
    def __init__(self, player_swap_delay, player_select_delay):
        '''
        class constructor
        This base class constructor should be called by the derived class constructor
        '''
        # must call base class constructor
        super().__init__(player_swap_delay, player_select_delay)
        # class variables
        self.player_states = []

    def register_player(self, game_board_state):
        '''
        Register a player to the game.
        :param game_board_state: the game board state of the player.
        '''
        self.player_states.append(self.PlayerState(game_board_state))

    def find_target(self, attacker):
        '''
        Find a valid target, given an attacking player
        The default implementation is to return the first player that is not the attacker.
        Can be overridden by the derived class.
        :param attacker: PlayerState, the attacking player
        '''
        for player in self.player_states:
            if player != attacker:
                return player
        assert False, "no valid target found in versus game"

    @abstractmethod
    def on_draw(self, screen):
        '''
        Draw the game state.
        :param screen: the pygame screen.
        '''

    def check_game_result_state(self):
        '''
        Method to invoke to check if the game has been decided.
        The default condition is "last man standing".
        Can be overridden by the derived class.
        :return: True if the game has been decided, False otherwise.
        '''
        # check all if all players are lost on the same tick
        # This may happen during a push_new_row_task
        if all([player.game_board_state.status.LOSE for player in self.player_states]):
            self.on_draw()
            return True
        # if the game is not decided yet...
        elif all([player.game_board_state.status.ACTIVE 
                  or player.game_board_state.status.INACTIVE
                  for player in self.player_states]):
            return False
        # if there are some losers...
        else:
            survivors = [player for player in self.player_states
                         if player.game_board_state.status != GameBoardState.Status.LOSE]
            if len(survivors) == 1:
                return True
            else:
                return False

    def game_end(self):
        '''
        notify players that the game is over.
        '''
        for i in range(len(self.player_states)):
            self.push_task(0, self.player_callback_task, i)

    def push_new_row_task(self):
        '''
        Add a new row to the game board
        '''
        for player in self.player_states:
            overflow = player.game_board_state.push_new_row(
                player.game_board_state.game_grid_state.column_count - 1
            )
            if overflow:
                player.game_board_state.status = GameBoardState.Status.LOSE
        # if the game is over
        if self.check_game_result_state():
            self.game_over = True
            self.game_end()
            # schedule the last task
            self.push_task(0, self.game_over_task)
        # if the game is not over...
        else:
            self.push_task(self.get_tick_between_new_row(), self.push_new_row_task)

    def check_player_callback(self):
        '''
        Check if all players callbacks are set.
        '''
        return all([player.player_callback is not None
                    for player in self.player_states])

    def set_player_callback(self, callback, player_id=1):
        '''
        Set the player callback
        :param callback: the callback function
        :param player_id: the player id (starts from 1)
        '''
        assert 0 < player_id <= len(self.player_states), "player id out of range"
        self.player_states[player_id - 1].player_callback = callback

    def player_callback_task(self, player_id):
        '''
        The callback task for the player
        :param player_id: the player id (starts from 1)
        '''
        assert 0 < player_id <= len(self.player_states), "player id out of range"
        # todo ...implement "get_grid()"


        
