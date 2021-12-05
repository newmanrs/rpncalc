import copy

from rpncalc.constantoperator import Constant
from rpncalc.idempotentoperator import IdempotentOperator
from rpncalc.unaryoperator import UnaryOperator
from rpncalc.binaryoperator import BinaryOperator
from rpncalc.reductionoperator import ReductionOperator
from rpncalc.linearalgebraoperator import LinearAlgebraOperator
from rpncalc.stackoperator import StackOperator
from rpncalc.history import HistoryOperator
from rpncalc.storedvalues import get_stored_value_class
from rpncalc.help import HelpOperator, HelpCommand, Help
from rpncalc.globals import stack


def compute_rpn(expression, verbose=False, return_copy=True):

    # Rollback the stack if parsing the expression throws
    # to preserve using the calculator in interactive mode
    backup = copy.deepcopy(stack)

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


def parse_expression(strexp, verbose=False):
    """
    Convert the string expression to numeric values or appropriate
    actions or operators for the calculator reverse polish evaluation loop.
    """

    # Arg could be one or more strings -- concatenate and split them
    if isinstance(strexp, list):
        strexp = ' '.join(strexp).split()
    else:
        strexp = strexp.split()

    if len(strexp) == 0:
        # No input -- feed calculator main help operator
        return [HelpOperator.print_main_help]

    parsedexp = []

    for arg in strexp:
        parsed = False
        for t in [int, float,
                  Constant,
                  BinaryOperator,
                  UnaryOperator,
                  IdempotentOperator,
                  ReductionOperator,
                  LinearAlgebraOperator,
                  StackOperator,
                  HistoryOperator,
                  get_stored_value_class,
                  Help]:
            try:
                parsedexp.append(t(arg))
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
    if not verbose:
        return parsedexp
    else:
        verboseexp = []
        for item in parsedexp:
            if isinstance(item, (int | float)):
                verboseexp.append(item)
            else:
                if (item != IdempotentOperator.print_stack or
                        not isinstance(item, HelpCommand)):
                    verboseexp.append(IdempotentOperator.print_stack)
                verboseexp.append(item)
        return verboseexp
