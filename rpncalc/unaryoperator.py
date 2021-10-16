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

        x = next(take_n(1,stack,self))

        match self.name:

            case 'sin':
                r = math.sin(x)
            case 'cos':
                r = math.cos(x)
            case 'tan':
                r = math.tan(x)
            case 'asin':
                r = math.asin(x)
            case 'exp':
                r = math.exp(x)
            case 'ln':
                r = math.log(x)
            case 'expmxsq':
                r = math.exp(-(x*x))
            case 'acos':
                r = math.acos(x)
            case 'atan':
                r = math.atan(x)
            case 'sqrt':
                r = math.sqrt(x)
            case 'to_int':
                r = int(x)
            case 'inv':
                r = 1.0/x
            case _:
                msg = f"Missing case match for {op}"
                raise NotImplementedError(msg)
        stack.append(r)

