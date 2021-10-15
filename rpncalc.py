import sys
import copy
import math
from enum import Enum, unique


class Constant:

    constants = {
        'pi'  : math.pi,
        'tau' : 2*math.pi,
        'c'   : 299792458,
        'h'   : 6.62607015e-34,
        'mu0' : 1.2566370621219e-6,
        'Na'  : 6.02214076e23,
        'kb'  : 1.380649e-23,
        'R'   : 8.314462618,
        'G'   : 6.6743015e-11,
        'g'   : 9.80665,
        'me'  : 9.109383701528e-31,
        'mp'  : 1.6726219236951e-27,
        'mn'  : 1.6749274980495e-27,
    }

    @classmethod
    def __call__(cls,arg):
        try:
            return cls.constants[arg]
        except KeyError:
            # Convert KeyError to ValueError to make this behave
            # like the enums below during argument parsing
            raise ValueError

@unique
class BinaryOperator(Enum):
    addition = '+'
    subtraction = '-'
    multiplication = '*'
    division = '/'
    integerdivision = '//'
    atan2 = 'atan2'        # atan2(y, x) input 1000 1 atan2 for ~pi/2
    log_base = 'log_base'  # 100 10 log_base gives 2

@unique
class UnaryOperator(Enum):
    sin = 'sin'
    cos = 'cos'
    tan = 'tan'
    acos = 'acos'
    asin = 'asin'
    atan = 'atan'
    to_int = 'int'
    exp = 'exp'
    expmxsq = 'expmxsq'    # exp(-x^2)
    ln = 'ln'
    sqrt = 'sqrt'

@unique
class IdempotentOperator(Enum):
    print_stack = 'print'


def parse_args(args):
    """
    Convert the initial list of argv[1:] to numeric values or appropriate actions
    or operators for the calculator reverse polish evaluation loop.
    """
    parsedargs = []

    for arg in args:
        parsed = False
        for t in [int, float, Constant(), BinaryOperator, UnaryOperator, IdempotentOperator]:
            try:
                parsedargs.append(t(arg))
                parsed = True
            except ValueError:
                pass
            else:
                break
        if not parsed:
            msg = f"Unknown operation parsing arg '{arg}'"
            raise ValueError(msg)

    return parsedargs

def take_n(n,stack, op):
    debug = copy.copy(stack)
    for i in range(n):
        try:
            yield stack.pop()
        except IndexError as e:
            msg = f"Empty stack processing {op} trying to pop {n} values. Stack: {debug}"
            raise IndexError(msg) from e

def binary_operator(op, stack):

    v1, v0 = tuple(take_n(2,stack,op))

    match op:

        case BinaryOperator.addition:
            r = v0+v1
        case BinaryOperator.subtraction:
            r = v0-v1
        case BinaryOperator.multiplication:
            r = v0*v1
        case BinaryOperator.division:
            r = v0/v1
        case BinaryOperator.integerdivision:
            r = v0//v1
        case BinaryOperator.log_base:
            r = math.log(v0,v1)
        case BinaryOperator.atan2:
            r = math.atan2(v0,v1)
        case _:
            msg = f"Missing case match for {op}"
            raise NotImplementedError(msg)

    stack.append(r)

def unary_operator(op, stack):

    x = tuple(take_n(1,stack,op))

    match op:

        case UnaryOperator.sin:
            r = math.sin(x)
        case UnaryOperator.cos:
            r = math.cos(x)
        case UnaryOperator.tan:
            r = math.tan(x)
        case UnaryOperator.asin:
            r = math.asin(x)
        case UnaryOperator.exp:
            r = math.exp(x)
        case UnaryOperator.ln:
            r = math.log(x)
        case UnaryOperator.expmxsq:
            r = math.exp(-(x*x))
        case UnaryOperator.acos:
            r = math.acos(x)
        case UnaryOperator.atan:
            r = math.atan(x)
        case UnaryOperator.sqrt:
            r = math.sqrt(x)
        case UnaryOperator.to_int:
            r = int(x)
        case _:
            msg = f"Missing case match for {op}"
            raise NotImplementedError(msg)
    stack.append(r)

def idempotent_operator(action, stack):

    match action:
        case IdempotentOperator.print_stack:
            print(f"Stack: {stack}")
        case _:
            msg = f"Missing case match for action {op}"
            raise NotImplementedError(msg)

def rpn(args):

    stack = []
    for arg in args:
        match arg:
            case _ if isinstance(arg, (int | float)):
                stack.append(arg)
            case _ if isinstance(arg, Constant):
                stack.append(arg)
            case _ if isinstance(arg, BinaryOperator):
                binary_operator(arg,stack)
            case _ if isinstance(arg, UnaryOperator):
                unary_operator(arg,stack)
            case _ if isinstance(arg, IdempotentOperator):
                idempotent_operator(arg, stack)
    return stack

def main():
    """
    RPN Calculator.  Entry point to script installed by setup.py.
    """

    if len(sys.argv) > 2: # Parse as given
        parsedargs = parse_args(sys.argv[1:])
    elif len(sys.argv) == 2: # Args encased in string
        parsedargs = parse_args(sys.argv[1].split())
    stack = rpn(parsedargs)

    #If only one item on stack, print value, otherwise print stack
    if len(stack) == 1:
        print(stack[0])
    else:
        print(stack)
