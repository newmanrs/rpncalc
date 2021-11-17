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
                # if verbose:
                #     parsedargs.append(IdempotentOperator.print_stack)

            except (ValueError, KeyError):
                # Parse fails from Constant() are KeyError, from the Enum
                # operator classes ValueErrors
                pass
            else:
                break
        if not parsed:
            msg = f"Unable to parse arg '{arg}'"
            raise ValueError(msg)

    # Program should add print statement to end of expression unless
    # one already exists.  If verbose, add print statements after all
    # operators, and last in series of int/floats
    if not verbose:
        # Final print - only print singular value if stack has one item
        iops = IdempotentOperator.print_stack
        iopsv = IdempotentOperator.print_stack_or_value
        if not (parsedexp[-1] == iops or parsedexp[-1] == iopsv):
            parsedexp.append(iopsv)
        return parsedexp
    else:  # verbose
        verboseexp = []
        for item in parsedexp:
            if isinstance(item, (int | float)):
                verboseexp.append(item)
            else:
                if item != IdempotentOperator.print_stack:
                    verboseexp.append(IdempotentOperator.print_stack)
                verboseexp.append(item)
        if verboseexp[-1] != IdempotentOperator.print_stack:
            verboseexp.append(IdempotentOperator.print_stack)
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
            f"Help for cmd {self.cmd}\n"
            f"Applies operator {self.op}\n"
            )
        if hasattr(self.op, 'help'):
            msg += self.op.help()
        print(msg)


class Help():

    def __call__(self, string):

        if string == 'help':
            return HelpOperator.print_main_help
        elif string.startswith('help(') and string.endswith(')'):
            cmd = string[5:-1]
            return HelpCommand(cmd)
        else:
            raise ValueError


Help = Help()
