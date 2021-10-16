import math, statistics
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

        o = type(self)
        match self:

            case o.reduce_plus:
                f = sum
            case o.reduce_mult:
                f = math.prod
            case o.mean:
                f = statistics.mean
            case o.reduce_max:
                f = max
            case o.reduce_min:
                f = min
            case o.stdev:
                f = statistics.stdev
            case o.sem:
                f = lambda x: statics.stdev(x)/sqrt(len(x))
            case o.variance:
                f = statistics.variance
            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)

        r = f(stack)
        stack.clear()
        stack.append(r)

