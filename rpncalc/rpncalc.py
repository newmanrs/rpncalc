import sys

from rpncalc.constants import Constants, get_constant_names
from rpncalc.idempotentoperator import IdempotentOperator
from rpncalc.unaryoperator import UnaryOperator
from rpncalc.binaryoperator import BinaryOperator
from rpncalc.reductionoperator import ReductionOperator
from rpncalc.storedvalues import get_stored_value_class


def parse_args(args):
    """
    Convert the initial list of argv[1:] to numeric values or appropriate
    actions or operators for the calculator reverse polish evaluation loop.
    """
    parsedargs = []

    for arg in args:
        parsed = False
        for t in [int, float,
                  Constants(),
                  BinaryOperator,
                  UnaryOperator,
                  IdempotentOperator,
                  ReductionOperator,
                  get_stored_value_class,
                  ]:
            try:
                parsedargs.append(t(arg))
                parsed = True
            except (ValueError, KeyError):
                # Parse fails from Constant() are KeyError, from the Enum
                # operator classes ValueErrors
                pass
            else:
                break
        if not parsed:
            msg = f"Unable to parse arg '{arg}'"
            raise ValueError(msg)

    if parsedargs[-1] != IdempotentOperator.print_stack:
        parsedargs.append(IdempotentOperator.print_stack)

    return parsedargs


def compute_rpn(args):

    stack = []
    for arg in args:
        match arg:
            case _ if isinstance(arg, (int | float)):
                stack.append(arg)
            case _ if hasattr(arg, 'action'):
                arg.action(stack)
            case _:
                msg = f"No known action in rpn parse loop for arg '{arg}'"
                raise ValueError(msg)
    return stack


def help():
    msg = "No arguments to parse. Displaying help.\n"
    msg += "Quote input to avoid shell expansion of special "
    msg += "chars such as '*', '>'\n"
    msg += "Pass integers or numbers to script and apply one or more"
    msg += " of the following operators:\n\n"
    msg += "Constants: {}\n\n".format(get_constant_names())
    msg += "Idempotent Operators: {}\n\n".format(
        tuple(i.value for i in IdempotentOperator))
    msg += "Unary Operators: {}\n\n".format(
        tuple(i.value for i in UnaryOperator))
    msg += "Binary Operators: {}\n\n".format(
        tuple(i.value for i in BinaryOperator))
    msg += "Reduction Operators: {}\n\n".format(
        tuple(i.value for i in ReductionOperator))
    msg += "Quote input to avoid shell expansion of "
    msg += "special chars such as '*', '>'"
    print(msg)


def main():
    """
    RPN Calculator.  Entry point to script installed by setup.py.
    """

    if len(sys.argv) > 2:  # Parse as given
        parsedargs = parse_args(sys.argv[1:])
    elif len(sys.argv) == 2:  # Args encased in string
        parsedargs = parse_args(sys.argv[1].split())
    else:
        help()
        sys.exit(0)

    stack = compute_rpn(parsedargs)

    # If only one item on stack, print value, otherwise print stack
    #if len(stack) == 1:
    #    print(stack[0])
    #else:
    #    print(stack)
