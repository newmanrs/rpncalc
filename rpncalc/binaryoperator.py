import math
from enum import Enum, unique
from rpncalc.util import take_n


@unique
class BinaryOperator(Enum):

    addition = '+'
    subtraction = '-'
    multiplication = '*'
    division = '/'
    integerdivision = '//'
    power = '^'
    atan2 = 'atan2'        # atan2(y, x) input 1000 1 atan2 for ~pi/2
    log_base = 'log_base'  # 100 10 log_base gives 2
    equals = '='
    gt = '>'
    gte = '>='
    lt = '<'
    lte = '<='
    choose = 'choose'
    combinations = 'combo'

    def action(self, stack):

        v1, v0 = tuple(take_n(2, stack, self))

        o = type(self)
        match self:

            case o.addition:
                r = v0+v1
            case o.subtraction:
                r = v0-v1
            case o.multiplication:
                r = v0*v1
            case o.division:
                r = v0/v1
            case o.integerdivision:
                r = v0//v1
            case o.power:
                r = math.pow(v0, v1)
            case o.log_base:
                r = math.log(v0, v1)
            case o.atan2:
                r = math.atan2(v0, v1)
            case o.equals:
                r = v0 == v1
            case o.gt:
                r = v0 > v1
            case o.gte:
                r = v0 >= v1
            case o.lt:
                r = v0 < v1
            case o.lte:
                r = v0 <= v1
            case o.choose:
                f = math.factorial
                r = f(v0)/(f(v0-v1))
            case o.combinations:
                f = math.factorial
                r = f(v0)/(f(v0-v1)*f(v1))
            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)

        stack.append(r)
