import argparse
import copy
# Ignore F401 import unused
# readline has sideeffects on builtin function 'input'
import readline  # noqa: F401
import traceback

from rpncalc.parseinput import parse_expression
from rpncalc.util import stack


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('expression', nargs='*')
    parser.add_argument('--help', '-h', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--interactive', '-i', action='store_true')
    parser.add_argument('--debug', action='store_true')

    return parser.parse_args()


def compute_rpn(expression, verbose=False, return_copy=True):
    backup = copy.deepcopy(stack)   # Rollback if expression throws
    try:
        for item in expression:
            match item:

                case _ if isinstance(item, (int | float)):
                    stack.append(item)
                case _ if hasattr(item, 'action'):
                    if verbose and hasattr(item, 'verbose_mode_message'):
                        item.verbose_mode_message()
                    item.action()
                case _:
                    s = f"No known action in rpn parse loop for item '{item}'"
                    raise ValueError(s)
    except Exception as e:
        stack.clear()
        for item in backup:
            stack.append(item)
        raise e

    if return_copy:
        return copy.deepcopy(stack)
    else:
        return stack


def interactive_loop(parser):
    while True:
        exp = input("Enter expression:\n")
        try:
            exp = parse_expression(exp, parser.verbose)
            if len(exp) > 0:
                ans = compute_rpn(exp, parser.verbose)
                print(f"Stack : {ans}")
        except Exception as e:
            traceback.print_exception(e)


def main():
    """
    RPN Calculator.  Entry point to script installed by setup.py.
    """

    parser = parse_args()

    if parser.interactive:
        interactive_loop(parser)

    exp = parse_expression(parser.expression, parser.verbose)
    ans = compute_rpn(exp, parser.verbose)
    print(f"Stack: {ans}")

    if parser.debug:
        breakpoint()
