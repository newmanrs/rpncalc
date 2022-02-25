import readline
import atexit
import os

import rpncalc.compute
from rpncalc.classes import ActionEnum
from rpncalc.state import state

HIST_LENGTH = 1000
HIST_LOC = '~/.local/rpncalc-history'

# Read history file and enable if successfully read
hist_file = os.path.expanduser(HIST_LOC)
history_enabled = False
try:
    readline.read_history_file(hist_file)
    history_enabled = True
except FileNotFoundError:
    print(
        f"No history file found at {HIST_LOC}."
        f" Create empty file at {HIST_LOC}"
        " to enable this feature"
        )
    # No file, return
except PermissionError:
    print(f"Permissions error on history file {hist_file}")

if history_enabled:

    readline.set_history_length(HIST_LENGTH)

    # Write to history on app close.
    # Consider rewriting with readline.append_history_file
    # to allow for concurrent interactive sessions
    atexit.register(readline.write_history_file, hist_file)


def print_history():

    if not history_enabled:
        print("History not enabled")
        return
    else:
        linecount = readline.get_current_history_length()
        maxchars = len(str(linecount))
        for i in range(linecount):
            idx = i+1
            line = readline.get_history_item(idx)
            msg = f"{idx:>{maxchars}} {line}"
            print(msg)


def get_history(idx: int):

    if not history_enabled:
        print('History not enabled')
        return
    else:
        maxidx = readline.get_current_history_length()
        if idx < 1 or idx > maxidx:
            msg = f"History idx must be between 1 and {maxidx}, received {idx}"
            print(msg)
        else:
            expr = readline.get_history_item(idx)
            print(f"Loaded history expr '{expr}'")
            rpncalc.compute._parse_expression(expr)


def last_history():

    if not history_enabled:
        print('History not enabled')
        return
    else:
        maxidx = readline.get_current_history_length()
        return readline.get_history_item(maxidx)


def add_to_history():
    """ Add command line history if not same as
    last prior command """
    last = last_history()
    if (s := state.expression) != last:
        readline.add_history(s)


class HistoryOperator(ActionEnum):

    print_history = 'history'
    get_history = 'get_history'

    def action(self):
        o = type(self)
        match self:
            case o.print_history:
                print_history()
            case o.get_history:
                idx = self.take_1()
                get_history(idx)

            case _:
                msg = f"Missing case match for action {self}"
                raise NotImplementedError(msg)
