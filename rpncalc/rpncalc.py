import argparse
# Ignore F401 import unused
# readline has sideeffects on builtin function 'input'
import readline  # noqa: F401
import traceback

from rpncalc.compute import compute
from rpncalc.history import add_to_history
from rpncalc.state import state, options


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('expression', nargs='*')
    parser.add_argument('--help', '-h', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--interactive', '-i', action='store_true')
    parser.add_argument('--load', '-l', type=str)
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    if args.help:
        raise NotImplementedError
    if args.verbose:
        options.verbose = True
    if args.interactive:
        options.interactive = True
    if args.load:
        options.load_file = args.load
    if args.debug:
        options.debug = True

    state.expression = ' '.join(args.expression)


def interactive_loop():

    while True:

        snapshot = state.make_snapshot()

        state.print_stack_and_stored()
        state.expression = input("Enter expression:\n")
        try:
            compute()
            if options.debug:
                breakpoint()
        except Exception as e:
            traceback.print_exception(e)
            print("Encountered above exception, reloading state snapshot")
            state.load_snapshot(snapshot)


def main():
    """
    RPN Calculator.  Entry point to script installed by setup.py.
    """

    # Parse input arguments into rpncalc.state.options
    parse_args()
    if f := options.load_file is not None:
        state.load_from_file(f)

    # Add command expression (if any) to history and run
    if state.expression:
        add_to_history()
        compute()

    if options.interactive:
        interactive_loop()

    state.print_stack_and_stored()
