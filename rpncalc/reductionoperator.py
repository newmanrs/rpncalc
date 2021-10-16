from statistics import stdev, variance
from math import sqrt
from enum import Enum, unique
from functools import reduce

@unique
class ReductionOperator(Enum):
    """
    Operators that convert n numeric values on the stack into one
    """
    reduce_plus = 'reduce+'
    reduce_mult = 'reduce*'
    mean        = 'mean'
    reduce_max  = 'max'
    reduce_min  = 'min'
    stdev       = 'stdev'
    sem         = 'sem'
    variance    = 'var'


    def action(self, stack):

        match self:
            case ReductionOperator.reduce_plus:
                r = reduce(lambda x,y: x+y, stack)
            case ReductionOperator.reduce_mult:
                r = reduce(lambda x,y: x*y, stack)
            case ReductionOperator.mean:
                r = reduce(lambda x,y: x+y, stack) / len(stack)
            case ReductionOperator.reduce_max:
                r = max(stack)
            case ReductionOperator.reduce_min:
                r = min(stack)
            case ReductionOperator.stdev:
                r = stdev(stack)
            case ReductionOperator.sem:
                r = stdev(stack) / sqrt(len(stack))
            case ReductionOperator.variance:
                r = variance(stack)
            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)

        stack.clear()
        stack.append(r)

