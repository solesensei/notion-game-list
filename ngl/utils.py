import json
import os
import sys
import time
from functools import wraps

from termcolor import colored

if sys.platform == "win32":
    import colorama
    os.system('color')
    colorama.init()


class ColorText:

    @staticmethod
    def r(msg):
        """ Returns red message """
        return colored(msg, "red")

    @staticmethod
    def g(msg):
        """ Returns green message """
        return colored(msg, "green")

    @staticmethod
    def y(msg):
        """ Returns yellow message """
        return colored(msg, "yellow")

    @staticmethod
    def c(msg):
        """ Returns cyan message """
        return colored(msg, "cyan")

    @staticmethod
    def m(msg):
        """ Returns magenta message """
        return colored(msg, "magenta")


class Echo:

    @staticmethod
    def _colored(msg, color):
        return colored(msg, color)

    @staticmethod
    def _color_print(msg, color, **kwargs):
        print(Echo._colored(msg, color=color), **kwargs)
        sys.stdout.flush()

    @staticmethod
    def r(msg, **kwargs):
        """ Print red color message """
        Echo._color_print(msg, "red", **kwargs)

    @staticmethod
    def g(msg, **kwargs):
        """ Print green color message """
        Echo._color_print(msg, "green", **kwargs)

    @staticmethod
    def y(msg, **kwargs):
        """ Print yellow color message """
        Echo._color_print(msg, "yellow", **kwargs)

    @staticmethod
    def c(msg, **kwargs):
        """ Print cyan color message """
        Echo._color_print(msg, "cyan", **kwargs)

    @staticmethod
    def m(msg, **kwargs):
        """ Print magenta color message """
        Echo._color_print(msg, "magenta", **kwargs)

    def __call__(self, *args, **kwargs):
        print(*args, **kwargs)
        sys.stdout.flush()


echo = Echo()
color = ColorText()


def load_from_file(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r') as f:
        return json.load(f)


def dump_to_file(d, filename):
    with open(filename, 'w') as f:
        json.dump(d, f)


def retry(exceptions, on_code=None, retry_num=3, initial_wait=0.5, backoff=2, raise_on_error=True, debug_msg=None, debug=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            _tries, _delay = retry_num + 1, initial_wait
            while _tries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    if on_code is not None and on_code != e.code:
                        if raise_on_error:
                            raise
                        return None
                    _tries -= 1
                    if _tries == 1:
                        if raise_on_error:
                            raise
                        return None
                    _delay *= backoff
                    if debug:
                        print_args = args if args else ""
                        msg = str(
                            f"Function: {f.__name__} args: {print_args}, kwargs: {kwargs}\n"
                            f"Exception: {e}\n"
                        ) if debug_msg is None else color.m(debug_msg)
                        echo.m("\n" + msg)
                        for s in range(_delay, 1, -1):
                            echo.m(" " * 20 + f"\rWait for {s} seconds!", end="\r")
                            time.sleep(1)
                    else:
                        time.sleep(_delay)
        return wrapper
    return decorator
