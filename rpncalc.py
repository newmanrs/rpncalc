import sys
import math
from enum import Enum, unique

@unique
class BinaryOperator(Enum):
    addition = '+'
    subtraction = '-'
    multiplication = '*'
    division = '/'
    integerdivision = '//'
    atan2 = 'atan2'
    log_base = 'log_base'


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
    expmxsq = 'expmxsq'
    ln = 'ln'
    sqrt = 'sqrt'

@unique
class NonaryOperator(Enum):
    stack = 'stack'


def parse_args(args):

    parsedargs = []

    for arg in args:
        parsed = False
        for t in [int, float, BinaryOperator, UnaryOperator, NonaryOperator]:
            try:
                parsedargs.append(t(arg))
                parsed = True
            except ValueError:
                pass
            else:
                break
        if not parsed:
            msg = f"Unknown operation parsing arg {arg}"
            raise ValueError(msg)
    return parsedargs

def binary_operator(op, stack):

    v1 = stack.pop()
    v0 = stack.pop()
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

    x = stack.pop()
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

def nonary_operator(action, stack):

    match action:
        case NonaryOperator.stack:
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
            case _ if isinstance(arg, BinaryOperator):
                binary_operator(arg,stack)
            case _ if isinstance(arg, UnaryOperator):
                unary_operator(arg,stack)
            case _ if isinstance(arg, NonaryOperator):
                nonary_operator(arg, stack)
    return stack

def main():
    """
    RPN Calculator.  Entry point to script installed by setup.py.
    """
    if len(sys.argv) > 2:
        parsedargs = parse_args(sys.argv[1:])
    if len(sys.argv) == 2:
        parsedargs = parse_args(sys.argv[1].split())
    stack = rpn(parsedargs)

    if len(stack) == 1:
        print(stack[0])
    else:
        print(stack)
