import math
from enum import Enum, unique
from rpncalc.util import take_n


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
    inv = 'inv'

    def action(self, stack):

        x = next(take_n(1, stack, self))

        o = type(self)
        match self:

            case o.sin:
                r = math.sin(x)
            case o.cos:
                r = math.cos(x)
            case o.tan:
                r = math.tan(x)
            case o.asin:
                r = math.asin(x)
            case o.exp:
                r = math.exp(x)
            case o.ln:
                r = math.log(x)
            case o.expmxsq:
                r = math.exp(-(x*x))
            case o.acos:
                r = math.acos(x)
            case o.atan:
                r = math.atan(x)
            case o.sqrt:
                r = math.sqrt(x)
            case o.to_int:
                r = int(x)
            case o.inv:
                r = 1.0/x
            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)
        stack.append(r)
