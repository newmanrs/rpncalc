from rpncalc.constantoperator import Constant
from rpncalc.idempotentoperator import IdempotentOperator
from rpncalc.unaryoperator import UnaryOperator
from rpncalc.binaryoperator import BinaryOperator
from rpncalc.reductionoperator import ReductionOperator
from rpncalc.linearalgebraoperator import LinearAlgebraOperator
from rpncalc.stateoperator import StateOperator
from rpncalc.randomoperator import RandomOperator
from rpncalc.history import HistoryOperator
from rpncalc.storedvalues import get_stored_value_class
from rpncalc.help import HelpOperator, Help
import rpncalc.state


def compute():
    _parse_expression()
    _compute_rpn()
    if rpncalc.state.options.debug:
        breakpoint()


def _compute_rpn():

    # Take state snapshot to roll back to if exceptions
    # are encountered
    verbose = rpncalc.state.options.verbose
    actions = rpncalc.state.state.actions

    while len(actions) > 0:

        action = actions.popleft()

        match action:

            case _ if isinstance(action, (int | float)):
                rpncalc.state.state.stack.append(action)

            case _ if hasattr(action, 'action'):
                if verbose and hasattr(action, 'verbose_mode_message'):
                    rpncalc.state.state.print_stack_and_stored()
                    action.verbose_mode_message()
                action.action()
                rpncalc.state.state.last_action = action.value

            case _:
                s = f"No known action in rpn parse loop for action '{action}'"
                raise ValueError(s)


def _string_to_type(arg: str):
    """
    Convert input to int, float, or calculator actions
    """
    for t in [int, float,
              Constant,
              BinaryOperator,
              UnaryOperator,
              IdempotentOperator,
              ReductionOperator,
              LinearAlgebraOperator,
              StateOperator,
              RandomOperator,
              HistoryOperator,
              get_stored_value_class,
              Help]:
        try:
            item = t(arg)
        except (ValueError, KeyError):
            # Parse fails from Constant() are KeyError, from the Enum
            # operator classes ValueErrors
            pass
        else:
            return item
    return None


def _parse_expression(exp=None):
    """
    Convert the string expression to numeric values or appropriate
    actions or operators for the calculator reverse polish evaluation loop.
    If the given expression is None, use expression stored in state
    """

    if exp is None:
        exp = rpncalc.state.state.expression

    tokens = exp.split()

    if len(tokens) == 0:
        # No tokens -- feed calculator main help operator
        return [HelpOperator.print_main_help]

    parsedexp = []

    for token in tokens:
        item = _string_to_type(token)
        if item is None:
            msg = f"Unable to parse token '{token} into a calculator action'"
            raise ValueError(msg)
        else:
            parsedexp.append(item)
    rpncalc.state.state.actions += parsedexp
