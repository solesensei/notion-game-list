import sys

from termcolor import colored, cprint

if sys.platform == 'win32':
    import colorama
    colorama.init()


class ColorText(object):

    @staticmethod
    def r(msg):
        """ Returns red message """
        return colored(msg, 'red')

    @staticmethod
    def g(msg):
        """ Returns green message """
        return colored(msg, 'green')

    @staticmethod
    def y(msg):
        """ Returns yellow message """
        return colored(msg, 'yellow')

    @staticmethod
    def c(msg):
        """ Returns cyan message """
        return colored(msg, 'cyan')

    @staticmethod
    def m(msg):
        """ Returns magenta message """
        return colored(msg, 'magenta')


class Echo(object):

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
        Echo._color_print(msg, 'red', **kwargs)

    @staticmethod
    def g(msg, **kwargs):
        """ Print green color message """
        Echo._color_print(msg, 'green', **kwargs)

    @staticmethod
    def y(msg, **kwargs):
        """ Print yellow color message """
        Echo._color_print(msg, 'yellow', **kwargs)

    @staticmethod
    def c(msg, **kwargs):
        """ Print cyan color message """
        Echo._color_print(msg, 'cyan', **kwargs)

    @staticmethod
    def m(msg, **kwargs):
        """ Print magenta color message """
        Echo._color_print(msg, 'magenta', **kwargs)

    def __call__(self, *args, **kwargs):
        print(*args, **kwargs)
        sys.stdout.flush()


echo = Echo()
color = ColorText()
