from statistics import stdev, variance
from math import sqrt
from enum import Enum, unique
from functools import reduce

@unique
class ReductionOperator(Enum):
    """
    Operators that convert n numeric values on the stack into one
    """
    reduce_plus = 'sum'
    reduce_mult = 'prod'
    mean        = 'mean'
    reduce_max  = 'max'
    reduce_min  = 'min'
    stdev       = 'stdev'
    sem         = 'sem'
    variance    = 'var'


    def action(self, stack):

        match self.name:

            case 'reduce_plus':
                r = reduce(lambda x,y: x+y, stack)
            case 'reduce_mult':
                r = reduce(lambda x,y: x*y, stack)
            case 'mean':
                r = reduce(lambda x,y: x+y, stack) / len(stack)
            case 'reduce_max':
                r = max(stack)
            case 'reduce_min':
                r = min(stack)
            case 'stdev':
                r = stdev(stack)
            case 'sem':
                r = stdev(stack) / sqrt(len(stack))
            case 'variance':
                r = variance(stack)
            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)

        stack.clear()
        stack.append(r)

