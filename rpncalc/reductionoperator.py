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

        o = ReductionOperator
        match self:

            case o.reduce_plus:
                r = reduce(lambda x,y: x+y, stack)
            case o.reduce_mult:
                r = reduce(lambda x,y: x*y, stack)
            case o.mean:
                r = reduce(lambda x,y: x+y, stack) / len(stack)
            case o.reduce_max:
                r = max(stack)
            case o.reduce_min:
                r = min(stack)
            case o.stdev:
                r = stdev(stack)
            case o.sem:
                r = stdev(stack) / sqrt(len(stack))
            case o.variance:
                r = variance(stack)
            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)

        stack.clear()
        stack.append(r)

