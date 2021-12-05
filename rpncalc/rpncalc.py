import argparse
# Ignore F401 import unused
# readline has sideeffects on builtin function 'input'
import readline  # noqa: F401
import traceback

from rpncalc.parseinput import compute_rpn, parse_expression


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('expression', nargs='*')
    parser.add_argument('--help', '-h', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--interactive', '-i', action='store_true')
    parser.add_argument('--debug', action='store_true')

    return parser.parse_args()


def interactive_loop(parser):
    while True:
        exp = input("Enter expression:\n")
        try:
            exp = parse_expression(exp, parser.verbose)
            if len(exp) > 0:
                ans = compute_rpn(exp, parser.verbose)
                print(f"Stack : {ans}")
                if parser.debug:
                    breakpoint()
        except Exception as e:
            traceback.print_exception(e)


def main():
    """
    RPN Calculator.  Entry point to script installed by setup.py.
    """

    parser = parse_args()

    if parser.interactive:
        interactive_loop(parser)
    else:
        readline.add_history(' '.join(parser.expression))
        exp = parse_expression(parser.expression, parser.verbose)
        ans = compute_rpn(exp, parser.verbose)
        print(f"Stack: {ans}")

    if parser.debug:
        breakpoint()
