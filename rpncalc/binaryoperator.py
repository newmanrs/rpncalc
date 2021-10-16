from enum import Enum, unique
from rpncalc.util import take_n

@unique
class BinaryOperator(Enum):
    addition = '+'
    subtraction = '-'
    multiplication = '*'
    division = '/'
    integerdivision = '//'
    atan2 = 'atan2'        # atan2(y, x) input 1000 1 atan2 for ~pi/2
    log_base = 'log_base'  # 100 10 log_base gives 2
    equals = '='
    gt     = '>'
    gte    = '>='
    lt     = '<'
    lte    = '<='

    def action(self, stack):

        v1, v0 = tuple(take_n(2,stack,self))

        match self:

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
            case BinaryOperator.equals:
                r = v0 == v1
            case BinaryOperator.gt:
                r = v0 > v1
            case BinaryOperator.gte:
                r = v0 >= v1
            case BinaryOperator.lt:
                r = v0 < v1
            case BinaryOperator.lte:
                r = v0 <= v1

            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)

        stack.append(r)

