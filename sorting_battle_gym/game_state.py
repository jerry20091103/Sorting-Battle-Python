from dataclasses import dataclass, field
from collections import namedtuple
from typing import Any
import queue

Coord = namedtuple('Coord', ['x', 'y'])

class GameState:
    '''
    This is the class that represents the whole game.
    Only this class should be used by the RL agent.
    '''

    @dataclass(order=True)
    class Task:
        tick: int
        callback: Any=field(compare=False)
        args: Any=field(compare=False)
        kwargs: Any=field(compare=False)

    def __init__(self, config):
        '''
        Constructor with config.
        '''
        # initialize the scheduler
        self.current_tick = 0
        self.task_queue = queue.PriorityQueue()
        self.test_count = 10
        # initialize the game
        self.swap_delay = config['swap_delay']
        self.remove_delay = config['remove_delay']
        self.player_callback = [None, None]
        # add the first task
        self.add_task(0, self.regular_callback)

    def regular_callback(self):
        '''
        The regular callback function.
        :param player_id: the player id.
        '''
        print("regular callback, test_count:", self.test_count)
        self.test_count -= 1
        if self.test_count > 0:
            self.add_task(5, self.regular_callback)

    def set_player_callback(self, callback, player_id=1):
        '''
        Set the callback function for RL agent.
        :param callback: the callback function.
        :param player_id: the player id. Default is 1.
        '''
        self.player_callback[player_id-1] = callback

    def handle_player_callback(self, player_id):
        '''
        Handle the callback function for RL agent.
        :param player_id: the player id.
        '''
        next_tick = self.player_callback[player_id](self.current_tick)
        self.add_task(next_tick, self.handle_player_callback, player_id)

    def add_task(self, tick, callback, *args, **kwargs):
        '''
        Add a task to the scheduler.
        :param tick: the tick to execute the task.
        :param callback: the callback function.
        :param args: the arguments for the callback function.
        :param kwargs: the keyword arguments for the callback function.
        '''
        new_task = self.Task(self.current_tick + tick, callback, args, kwargs)
        self.task_queue.put(new_task)

    def run_game(self):
        '''
        Run the game.
        '''
        assert self.player_callback[0] or self.player_callback[1], "no player callback is set"
        if self.player_callback[0] is not None:
            self.handle_player_callback(0)
        if self.player_callback[1] is not None:
            self.handle_player_callback(1)
        # run scheduler
        while not self.task_queue.empty():
            task = self.task_queue.get()
            assert task.tick >= self.current_tick, "scheduler is out of order"
            self.current_tick = task.tick
            print('tick: ', self.current_tick)
            task.callback(*task.args, **task.kwargs)
            if self.current_tick > 50:
                break
