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

    def action(self, stack):

        x = next(take_n(1,stack,self))

        match self:

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

