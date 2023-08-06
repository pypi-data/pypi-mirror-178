import six
import click
import collections

from pyfiglet import figlet_format
from PyInquirer import Token, style_from_dict

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    def colored(string, color=None, highlights=None):
        return string


def log(string, color="white", font="slant", figlet=False):
    if not figlet:
        six.print_(colored(string, color))
    else:
        six.print_(colored(figlet_format(string, font=font), color))


class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands


style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})

