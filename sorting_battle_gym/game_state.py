'''
This moduel defines the abstract base class for all game modes and represents the whole game.
Also defines Coord type for coordinates.
'''
from dataclasses import dataclass, field
from collections import namedtuple
from typing import Any
from abc import ABC, abstractmethod
from time import sleep
import queue
import numpy as np

Coord = namedtuple('Coord', ['x', 'y'])

class GameState(ABC):
    '''
    This is Abstract base class for all game modes and represents the whole game.
    Also provides a tick based task scheduler.
    '''
    @dataclass(order=True)
    class Task:
        '''
        This class represents a task in the scheduler.
        '''
        tick: int
        callback: Any=field(compare=False)
        args: Any=field(compare=False)
        kwargs: Any=field(compare=False)

    def __init__(self, player_swap_delay, player_select_delay, player_add_new_row_delay):
        '''
        Constructor with config.
        '''
        # initialize the scheduler
        self.current_tick = 0
        self.task_queue = queue.PriorityQueue()
        # init common game parameters
        self.player_swap_delay = player_swap_delay
        self.player_select_delay = player_select_delay
        self.player_add_new_row_delay = player_add_new_row_delay
        self.level = 0
        self.game_over = False
        self.end_scheduler = False

    def run_game(self, realtime):
        '''
        Run the game.
        '''
        # run scheduler
        while not self.task_queue.empty():
            task = self.task_queue.get()
            assert task.tick >= self.current_tick, "scheduler is out of order"
            # use a very simple sleep to simulate realtime for now...
            if realtime:
                sleep((task.tick - self.current_tick) * 0.02)
            self.current_tick = task.tick
            # *print task name for debug
            # print('# tick:', self.current_tick, task.callback.__name__)
            task.callback(*task.args, **task.kwargs)
            if self.end_scheduler:
                break

    def push_task(self, tick, callback, *args, **kwargs):
        '''
        Add a task to the scheduler.
        :param tick: the tick to execute the task.
        :param callback: the callback function.
        :param args: the arguments for the callback function.
        :param kwargs: the keyword arguments for the callback function.
        '''
        new_task = self.Task(self.current_tick + tick, callback, args, kwargs)
        self.task_queue.put(new_task)

    def level_up_task(self):
        '''
        Level up the game.
        '''
        self.level += 1
        self.push_task(self.get_tick_between_level_up(), self.level_up_task)

    def game_over_task(self):
        '''
        Game over. This task will be the last task in the scheduler.
        '''
        self.end_scheduler = True

    @abstractmethod
    def game_end(self):
        '''
        notify players that the game is over.
        '''

    @abstractmethod
    def push_new_row_task(self):
        '''
        Add a new row to the game board
        '''

    @abstractmethod
    def push_one_row_task(self, player_id):
        '''
        Push one row to the game board.
        :param player_id: the player id.
        '''

    @abstractmethod
    def set_player_callback(self, callback, player_id=1):
        '''
        Set the callback function for RL agent.
        :param callback: the callback function.
        :param player_id: the player id. Default is 1.
        '''

    @abstractmethod
    def check_player_callback(self):
        '''
        Check if the callback all required player callbacks are set.
        :return: True if all required player callbacks are set.
        '''

    @abstractmethod
    def player_callback_task(self, player_id):
        '''
        Handle the callback function for RL agent.
        :param player_id: the player id.
        '''

    def init_tasks(self):
        '''
        Add required initial tasks when the game starts.
        Must be called from the subclass.
        '''
        self.push_task(self.get_tick_between_level_up(), self.level_up_task)
        self.push_task(self.get_tick_between_new_row(), self.push_new_row_task)

    def get_tick_between_new_row(self):
        '''
        Get the tick between new row.
        '''
        return int(round(150 - 90 * np.clip(np.power(self.level/20, 4), 0, 1)))

    def get_tick_between_level_up(self):
        '''
        Get the tick between level up.
        '''
        return 300

    def handle_player_action(self, player, player_id, action_type, action_data):
        '''
        Handle the action from the player.
        :param player: the player. Contains a GameBoardState
        :param action_id: the action id.
        :param action_data: the action data.
        '''
        try:
            action_delay = 0
            if action_type == 0: # idle
                action_delay = action_data
            elif action_type == 1: # swap
                assert len(action_data) == 2, "action_data must contain 2 coordinates when swapping"
                coord1 = Coord(action_data[0][0], action_data[0][1])
                coord2 = Coord(action_data[1][0], action_data[1][1])
                assert player.game_board_state.game_controller_state.swap([coord1, coord2]), "invalid swap"
                action_delay = self.player_swap_delay
            elif action_type == 2: # select
                assert action_data is not None, "action_data must not be None when selecting"
                (tile_number, garbage_number) = player.game_board_state.game_controller_state.select(action_data)
                action_delay = self.player_select_delay
                assert tile_number > 0, "invalid select"
            elif action_type == 3: # add_new_row
                self.push_task(0, self.push_one_row_task, player_id)
                action_delay = self.player_add_new_row_delay

            # schedule the next callback
            self.push_task(action_delay, self.player_callback_task, player_id)
        except AssertionError as error:
            # pause the game and show the error message
            print("[ERROR] in player_callback_task:", error)
            # print action type and data
            print("action_type:", action_type, ", action_data:", action_data)
            input("The previous callback wiil be sent again. Press any key to continue...")
            self.push_task(0, self.player_callback_task, player_id)
