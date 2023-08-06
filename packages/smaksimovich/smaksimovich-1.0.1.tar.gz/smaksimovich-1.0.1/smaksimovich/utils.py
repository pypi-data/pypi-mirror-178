from collections import defaultdict
from typing import Iterable
from dataclasses import dataclass
from datetime import timedelta
import numpy as np
import pandas as pd
import json
import math
import time



def json_loadf(file_path: str):
    """ Parses a JSON file into a dictionary

    Args:
        file_path (string): path to the JSON file

    Returns:
        dict: the parsed JSON object
    """
    with open(file_path, "r") as file:
        return json.loads(file.read())


def json_savef(object: dict, file_path: str):
    """ Saves a dictionary as a JSON file

    Args:
        object (dict): the object to save as JSON
        file_path (str): the path to the JSON file to save in
    """
    with open(file_path, "w") as file:
        file.write(json.dumps(object))


def unzip(iterable: Iterable):
    """ The opposite of zip.
    Example:
        >>> time_temperature = [['7/22', 54], ['7/23', 55], ['7/24', 43]]
        >>> time, temp = unzip(time_temperature)
        >>> time
        ['7/22', '7/23', '7/24']
        >>> temp
        [54, 55, 43]

    Args:
        iterable (Iterable): the object to unzip

    Returns:
        List: the unzipped list
    """
    return list(zip(*iterable))


def wrap(x: float, high: float):
    """ Clips x on the domain [-high, high], repeating itself 
    See this graph to understand better
    https://www.desmos.com/calculator/qruhpbx45y

    Args:
        x (float): a number to wrap
        high (float): the maximum value of x
    """
    return ((x - high) % (2 * high)) - high


def discretize(x: float, lo: float, hi: float, n: float):
    """ Returns index of x between lo and hi divided by n
    """
    index = math.floor((x - lo) / (hi - lo) * n)
    return np.clip(index, 0, n - 1)


def staircase(x, y):
    """ Given a list of (x, y) coordinates, this function will return
    a list xy coordinates that, when plotted, show a staircase of xy

    Args:
        x (List[float]): list of x coordinates
        y (List[float]): list of y coordinates
    """
    assert len(x) == len(y), "Expected x and y to have same length"
    if len(x) <= 1:
        return x, y

    xy = sorted(zip(x, y), key=lambda t: t[0])
    x_res = [xy[0][0]]
    y_res = [xy[0][1]]
    for i in range(1, len(xy)):
        x_prev, y_prev = xy[i - 1]
        x_curr, y_curr = xy[i]

        x_res.append((x_prev + x_curr) / 2)
        y_res.append(y_prev)

        x_res.append((x_prev + x_curr) / 2)
        y_res.append(y_curr)

        x_res.append(x_curr)
        y_res.append(y_curr)

    return x_res, y_res    


def flatten(iterable):
    """ Flattens an iterable

    Args:
        iterable (Iterable): the iterable to flatten

    Returns:
        List[any]: the flatten list of items
    """
    if type(iterable) == str:
        return [iterable]
    res = []
    try:
        iterator = iter(iterable)
    except TypeError:
        return [iterable]
    else:
        for i in iterator:
            res += flatten(i)
    return res


def progress(iteration, total_iterations, time_elapsed=None, percent_to_progress=0.05, time_to_progress=timedelta(minutes=1)):
    """ Evaluates whether a progress bar has progressed enough to print
        a notification. Returns true if the progress bar has progressed enough percent
        or if enough time has elapsed
        
        Args:
            iteration (int): the current iteration
            total_iterations (int): the number of iterations that will be completed
            time_elapsed (float): the amount of time that has elapsed since the last notification (seconds)
            percent_to_progress (float): the minimum amount of progress needed to print a notification
            time_to_progress (float): the minimum amount of time needed to print a notification
    """
    time_elapsed = timedelta(seconds=time_elapsed)
    if time_elapsed >= time_to_progress:
        return True

    # progress implies the iteration is a multiple of floor(percent * total_iterations)
    steps_per_progress = math.floor(percent_to_progress * total_iterations)
    if steps_per_progress == 0 or iteration % steps_per_progress == 0:
        return True

    return False


def p_assert(res, expected):
    assert res == expected, f"Expected result\n{res}\nto equal expected\n{expected}"


class Timer:
    ONE_SECOND = 1
    ONE_MINUTE = 60
    ONE_HOUR = 3600

    @dataclass
    class StopWatch: 
        t_start : float = 0
        t_end   : float = 0
        running : bool  = False

        def start(self):
            self.t_start = time.time()
            self.running = True

        def stop(self):
            self.t_end = time.time()
            self.running = False

        def elapsed(self) -> float:
            if self.running:
                return time.time() - self.t_start
            else:
                return self.t_end - self.t_start

        @staticmethod
        def format_time_string(seconds: float) -> str:
            if seconds < Timer.ONE_SECOND:
                return f"{seconds*1000:3.0f}ms"
            elif seconds < Timer.ONE_MINUTE:
                return f"{seconds:>4.1f}s"
            elif seconds < Timer.ONE_HOUR:
                minutes, seconds = divmod(seconds, Timer.ONE_MINUTE)
                return f"{minutes:>2.0f}m {seconds:_>2.0f}s"
            else:
                hours, remainder = divmod(seconds, Timer.ONE_HOUR)
                minutes, seconds = divmod(remainder, Timer.ONE_MINUTE)
                return f"{hours:02.0f}h {minutes:02.0f}m {seconds:02.0f}s"

        def __str__(self):
            return Timer.StopWatch.format_time_string(self.elapsed())

        def progress(self, iteration, total_iteration, **kwargs):
            res = progress(iteration, total_iteration, self.elapsed(), **kwargs)
            self.start()
            return res

    DEFAULT_NAME = 'Timer_Default_Name'
    timer_map = defaultdict(lambda: Timer.StopWatch())

    @staticmethod
    def start(name=DEFAULT_NAME):
        Timer.timer_map[name].start()

    @staticmethod
    def stop(name=DEFAULT_NAME):
        Timer.timer_map[name].stop()

    @staticmethod
    def str(name=DEFAULT_NAME) -> str:
        return str(Timer.timer_map[name])

    @staticmethod
    def elapsed(name=DEFAULT_NAME) -> float:
        return Timer.timer_map[name].elapsed()

    @staticmethod
    def progress(iteration, total_iteration, name=DEFAULT_NAME, **kwargs) -> bool:
        return Timer.timer_map[name].progress(iteration, total_iteration, **kwargs)


class Profiler:

    def __init__(self):
        self.df = pd.DataFrame(columns=["fn", "  total time (ms)", "  avg time (ms)", "ncalls"])

    def timeit(self, fn, *args, ncalls=1000):
        res = []
        for i in range(ncalls):
            s = time.time_ns()
            fn(*args)
            e = time.time_ns()
            res.append(e - s)
        return np.array(res)

    def profile(self, fn, *args, ncalls):
        t = self.timeit(fn, *args, ncalls=ncalls)
        total = np.sum(t) / 10**6
        avg = total / ncalls
        self.df = pd.concat([pd.DataFrame([[fn.__name__, f"{total:.3f}", f"{avg:.3f}", ncalls]], columns=self.df.columns), self.df], ignore_index=True)

    def __str__(self):
        return str(self.df)