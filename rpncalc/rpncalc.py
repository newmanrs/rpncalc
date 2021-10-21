import argparse

from rpncalc.constants import Constants, get_constant_names
from rpncalc.idempotentoperator import IdempotentOperator
from rpncalc.unaryoperator import UnaryOperator
from rpncalc.binaryoperator import BinaryOperator
from rpncalc.reductionoperator import ReductionOperator
from rpncalc.linearalgebraoperator import LinearAlgebraOperator
from rpncalc.storedvalues import get_stored_value_class
from rpncalc.util import stack


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('expression', nargs='*')
    parser.add_argument('--help', '-h', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--debug', action='store_true')

    return parser.parse_args()


def parse_expression(exp, verbose=False):
    """
    Convert the string expression to numeric values or appropriate
    actions or operators for the calculator reverse polish evaluation loop.
    """

    # Arg could be one or more strings - concatenate and split them
    exp = ' '.join(exp).split()

    parsedargs = []

    for arg in exp:
        parsed = False
        for t in [int, float,
                  Constants(),
                  BinaryOperator,
                  UnaryOperator,
                  IdempotentOperator,
                  ReductionOperator,
                  LinearAlgebraOperator,
                  get_stored_value_class,
                  ]:
            try:
                parsedargs.append(t(arg))
                parsed = True
                if verbose:
                    parsedargs.append(IdempotentOperator.print_stack)
            except (ValueError, KeyError):
                # Parse fails from Constant() are KeyError, from the Enum
                # operator classes ValueErrors
                pass
            else:
                break
        if not parsed:
            msg = f"Unable to parse arg '{arg}'"
            raise ValueError(msg)

    iops = IdempotentOperator.print_stack
    iopsv = IdempotentOperator.print_stack_or_value
    if not (parsedargs[-1] == iops or parsedargs[-1] == iopsv):
        parsedargs.append(IdempotentOperator.print_stack_or_value)

    return parsedargs


def compute_rpn(expression, verbose=False):

    for item in expression:
        match item:

            case _ if isinstance(item, (int | float)):
                stack.append(item)
            case _ if hasattr(item, 'action'):
                if verbose and not item == IdempotentOperator.print_stack:
                    print(f"Applying {item}")
                item.action()
            case _:
                msg = f"No known action in rpn parse loop for item '{item}'"
                raise ValueError(msg)
    return stack


def help():

    c = get_constant_names()
    io = tuple(i.value for i in IdempotentOperator)
    uo = tuple(i.value for i in UnaryOperator)
    bo = tuple(i.value for i in BinaryOperator)
    ro = tuple(i.value for i in ReductionOperator)
    lao = tuple(i.value for i in LinearAlgebraOperator)

    msg = (
        "Displaying help.\n"
        "Quote input to avoid shell expansion of special "
        "chars such as '*', '>'\n"
        "Pass integers or numbers to script and apply one or more"
        " of the following operators:\n\n"
        f"Constants: {c}\n\n"
        f"Idempotent Operators: {io}\n\n"
        f"Unary Operators: {uo}\n\n"
        f"Binary Operators: {bo}\n\n"
        f"Reduction Operators: {ro}\n\n"
        f"Linear Algebra Operators {lao}\n\n"
        "Quote input to avoid shell expansion of "
        "special chars such as '*', '>'"
        )

    print(msg)


def main():
    """
    RPN Calculator.  Entry point to script installed by setup.py.
    """

    parser = parse_args()
    if parser.help or len(parser.expression) == 0:
        help()
    else:
        exp = parse_expression(parser.expression, parser.verbose)
        compute_rpn(exp, parser.verbose)

    if parser.debug:
        breakpoint()
