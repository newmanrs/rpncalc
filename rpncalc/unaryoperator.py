import math
from enum import Enum, unique
from rpncalc.util import take_n


def expmxsq(x):
    return math.exp(-(x*x))


def inv(x):
    return 1.0/x


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
    fact = '!'
    ln = 'ln'
    sqrt = 'sqrt'
    inv = 'inv'

    def action(self, stack):

        x = next(take_n(1, stack, self))

        o = type(self)
        match self:

            case o.sin:
                f = math.sin
            case o.cos:
                f = math.cos
            case o.tan:
                f = math.tan
            case o.asin:
                f = math.asin
            case o.exp:
                f = math.exp
            case o.ln:
                f = math.log
            case o.expmxsq:
                f = expmxsq
            case o.fact:
                f = math.factorial
            case o.acos:
                f = math.acos
            case o.atan:
                f = math.atan
            case o.sqrt:
                f = math.sqrt
            case o.to_int:
                f = int
            case o.inv:
                f = inv
            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)
        stack.append(f(x))
