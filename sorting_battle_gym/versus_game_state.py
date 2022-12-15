from abc import abstractmethod
from sorting_battle_gym.game_state import GameState
from sorting_battle_gym.game_board_state import GameBoardState
import numpy as np

class VersusGameState(GameState):
    '''
    Abstract base classes for game modes that have more than 1 player.
    It inherits the abstract base class GameState.
    '''
    class PlayerState:
        '''
        This class represents a player in VersusGameState.
        '''
        PRESSURE_TICK_DURATION = 120
        MAX_PRESSURE_PER_ATTACK = 20
        GARBAGE_PER_ADDITIONAL_ROW = 10

        def __init__(self, game_state, game_board_state):
            '''
            class constructor
            :param game_state: the GameState object, should be its own parent
            :param game_board_state: the GameBoardState object of the player
            '''
            self.game_state = game_state
            self.game_board_state = game_board_state
            self.last_pressure_tick = 0
            self.player_callback = None
            # Load per-player events here.
            self.game_state.push_task(0, self.load_task)
            self.game_state.push_task(1, self.check_receive_garbage_task)
            # set attack() as the callback function for score increase
            self.game_board_state.game_score_state.set_score_increase_callback(self.attack)

        def reset_pressure_tick(self):
            '''
            Reset player's pressure tick.
            This function needs to be called when pressure changes.
            '''
            self.last_pressure_tick = self.game_state.tick

        def attack(self, score_increase_info):
            '''
            Attack the other player.
            This function needs to be called by GameScoreState when the score increase.
            :param score_increase_info: tuple(score_increase, remove_count, combo)
            '''
            # Find a target to attack.
            target = self.game_state.find_target(self)
            # Use GamePressureState.Attack to transfer pressure to target.
            self.game_board_state.game_pressure_state.attack( \
                other = target.game_board_state.game_pressure_state, \
                attack_power = self.compute_attack_power(score_increase_info) \
            )
            # Reset target's pressure tick.
            target.reset_pressure_tick()

        def compute_attack_power(self, score_increase_info):
            '''
            Compute the attack power.
            :param score_increase_info: tuple(score_increase, remove_count, combo)
            :return: the attack power
            '''
            remove_count = score_increase_info[1]
            combo = score_increase_info[2]
            return int(remove_count + combo / 2)

        def compute_attack_load(self, pressure_consumed):
            '''
            Compute the attack load based on the consumed pressure.
            :param pressure_consumed: the consumed pressure
            :return: (int: num_garbage_rows, int: num_garbage_columns)
            '''
            if pressure_consumed > 0:
                num_garbage_rows = 1 + pressure_consumed // VersusGameState.PlayerState.GARBAGE_PER_ADDITIONAL_ROW
                # lerp(1, 4, pressure_consumed % 10 / 10)
                column_count = self.game_board_state.game_grid_state.column_count
                pressure_ramainder = pressure_consumed % VersusGameState.PlayerState.GARBAGE_PER_ADDITIONAL_ROW
                num_garbage_columns = int(round(1 + (column_count - 2) * np.clip( float(pressure_ramainder)/float(10), 0, 1)))
            else:
                num_garbage_rows = 0
                num_garbage_columns = 0
            return num_garbage_rows, num_garbage_columns

        def load_task(self):
            '''
            Task to load the game board with random numbers.
            '''
            self.game_board_state.game_grid_state.load_random(0.8)

        def check_receive_garbage_task(self):
            '''
            Check if the player needs to receive garbage from pressure.
            '''
            overflow = False
            # if time exceeds the pressure tick duration
            if self.game_state.tick - self.last_pressure_tick >= VersusGameState.PlayerState.PRESSURE_TICK_DURATION:
                # Can dump garbage from pressure.
                pressure_consumed = self.game_board_state.game_pressure_state.consume_pressure(VersusGameState.PlayerState.MAX_PRESSURE_PER_ATTACK)
                garbage_rows, garbage_columns = self.compute_attack_load(pressure_consumed)
                if garbage_rows > 0:
                    overflow = self.game_board_state.push_garbage_rows(garbage_rows, garbage_columns)
                # Because we consumed pressure, we have to reset pressure tick here.
                self.reset_pressure_tick()
            # after garbage is received, check if the game is over
            if overflow:
                self.game_board_state.status = GameBoardState.Status.LOSE
                if self.game_state.check_game_result_state():
                    self.game_state.game_over = True
                    self.game_state.game_end()
                    # schedule the last task
                    self.game_state.push_task(0, self.game_state.game_over_task)
            else:
                self.game_state.push_task(1, self.check_receive_garbage_task)

    
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
        self.player_states.append(self.PlayerState(self, game_board_state))

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
    def on_draw(self):
        '''
        Method to invoke when the game ends in a draw.
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
        if all(player.game_board_state.status.LOSE for player in self.player_states):
            self.on_draw()
            return True
        # if the game is not decided yet...
        if all(player.game_board_state.status.ACTIVE
                  or player.game_board_state.status.INACTIVE
                  for player in self.player_states):
            return False
        # if there are some losers...
        survivors = [player for player in self.player_states
                     if player.game_board_state.status != GameBoardState.Status.LOSE]
        if len(survivors) == 1:
            return True
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
        return all(player.player_callback is not None
                   for player in self.player_states)

    def set_player_callback(self, callback, player_id=1):
        '''
        Set the player callback
        :param callback: the callback function
        :param player_id: the player id (starts from 1)
        '''
        assert 0 < player_id <= len(self.player_states), "player id out of range"
        self.player_states[player_id - 1].player_callback = callback
