from rpncalc.constants import Constant
from rpncalc.idempotentoperator import IdempotentOperator
from rpncalc.unaryoperator import UnaryOperator
from rpncalc.binaryoperator import BinaryOperator
from rpncalc.reductionoperator import ReductionOperator
from rpncalc.linearalgebraoperator import LinearAlgebraOperator
from rpncalc.stackoperator import StackOperator
from rpncalc.storedvalues import get_stored_value_class
from rpncalc.util import ActionEnum


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


def help_string():

    c = tuple(i.value for i in Constant)
    io = tuple(i.value for i in IdempotentOperator)
    uo = tuple(i.value for i in UnaryOperator)
    bo = tuple(i.value for i in BinaryOperator)
    ro = tuple(i.value for i in ReductionOperator)
    lao = tuple(i.value for i in LinearAlgebraOperator)
    so = tuple(i.value for i in StackOperator)

    msg = (
        "Displaying help.\n"
        "Pass integers or numbers to script and apply one or more"
        " of the following operators:\n"
        f"Idempotent Operators: {io}\n"
        f"Unary Operators: {uo}\n"
        f"Binary Operators: {bo}\n"
        f"Reduction Operators: {ro}\n"
        f"Linear Algebra Operators {lao}\n"
        f"Stack Operators {so}\n"
        f"Constants: {c}\n"
        "--verbose, -v, to show how the stack is processed\n"
        "--interactive, -i, for interactive input loop"
        )

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
        self.op = parse_expression(cmd)[0]

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
