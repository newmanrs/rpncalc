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
    gt     = '>'
    gte    = '>='
    lt     = '<'
    lte    = '<='

    def action(self, stack):

        v1, v0 = tuple(take_n(2,stack,self))

        match self.name:

            case 'addition':
                r = v0+v1
            case 'subtraction':
                r = v0-v1
            case 'multiplication':
                r = v0*v1
            case 'division':
                r = v0/v1
            case 'integerdivision':
                r = v0//v1
            case 'power':
                r = math.pow(v0,v1)
            case 'log_base':
                r = math.log(v0,v1)
            case 'atan2':
                r = math.atan2(v0,v1)
            case 'equals':
                r = v0 == v1
            case 'gt':
                r = v0 > v1
            case 'gte':
                r = v0 >= v1
            case 'lt':
                r = v0 < v1
            case 'lte':
                r = v0 <= v1

            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)

        stack.append(r)

