import rpncalc.parseinput

from rpncalc.classes import ActionEnum
from rpncalc.constantoperator import Constant
from rpncalc.idempotentoperator import IdempotentOperator
from rpncalc.unaryoperator import UnaryOperator
from rpncalc.binaryoperator import BinaryOperator
from rpncalc.reductionoperator import ReductionOperator
from rpncalc.linearalgebraoperator import LinearAlgebraOperator
from rpncalc.stackoperator import StackOperator
from rpncalc.history import HistoryOperator

import shutil
import textwrap


def get_terminal_width():
    return shutil.get_terminal_size().columns


def help_string():

    # textwrap is called to wrap individual sentences which
    # means be careful with commas separating the sentences
    # in the list while using implicit concatentation
    msg = [
        "Displaying help.",
        "Pass integers or numbers to script and apply one or more"
        " of the following operators:"
        ]
    msg_foot = [
        "Use help(cmd) or help_cmd for help on specific operators"
        " such as help_matsq\n",
        "--verbose, -v, to show how the stack is processed",
        "--interactive, -i, for interactive input loop",
        "--debug, for breakpoints after expression evalution",
        ]

    tx = textwrap.TextWrapper(
        width=get_terminal_width(),
        subsequent_indent=' '
        )

    msg = '\n'.join([tx.fill(i) for i in msg])
    msg += '\n' + operator_help_list() + '\n'
    msg += '\n'.join([tx.fill(i) for i in msg_foot])

    return msg


def operator_help_list():
    msg = ''
    types = [
        BinaryOperator, UnaryOperator,
        IdempotentOperator, ReductionOperator,
        LinearAlgebraOperator, Constant,
        StackOperator, HistoryOperator
        ]
    for T in types:
        msg += ' ' + T.__name__ + 's:\n'
        msg += textwrap.fill(
            ', '.join(i.value for i in T),
            get_terminal_width(),
            initial_indent='  ',
            subsequent_indent='  '
            )
        msg += '\n'
    return msg


class HelpOperator(ActionEnum):
    print_main_help = 'help'

    def action(self):
        o = type(self)
        match self:
            case o.print_main_help:
                print(help_string())
            case _:
                msg = f"Missing case match for action {self}"
                raise NotImplementedError(msg)


class HelpCommand():

    def __init__(self, cmd):
        self.cmd = cmd
        self.op = rpncalc.parseinput.parse_expression(cmd)[0]

    def action(self):
        # Print what we know about the command
        msg = (
            f"Help for cmd '{self.cmd}'\n"
            f"Applies operator {self.op}."
            )
        if hasattr(self.op, 'help'):
            if m := self.op.help():
                msg += m
        print(msg)


class Help():

    def __call__(self, string):

        if string == 'help':
            return HelpOperator.print_main_help
        elif string.startswith('help(') and string.endswith(')'):
            cmd = string[5:-1]
            return HelpCommand(cmd)
        elif string.startswith('help_'):
            cmd = string[5:]
            return HelpCommand(cmd)
        else:
            raise ValueError


Help = Help()
