import numpy
import functools
from rpncalc.classes import ActionEnum


def sem(x):
    return numpy.std(x, ddof=1) / numpy.sqrt(len(x)-1)


class ReductionOperator(ActionEnum):
    """
    Operators that convert n numeric values on the stack into one
    """

    reduce_plus = 'sum'
    reduce_mult = 'prod'
    mean = 'mean'
    reduce_max = 'max'
    reduce_min = 'min'
    stdev = 'stdev', "Sample standard deviation (N-1 DoF)"
    sem = 'sem', "Sample standard error of the mean (N-1 DoF)"
    variance = 'var', "Sample variance (N-1 DoF)"

    def action(self):

        o = type(self)
        match self:

            case o.reduce_plus:
                f = numpy.sum
            case o.reduce_mult:
                f = numpy.prod
            case o.mean:
                f = numpy.mean
            case o.reduce_max:
                f = numpy.max
            case o.reduce_min:
                f = numpy.min
            case o.stdev:
                f = functools.partial(numpy.std, ddof=1)
            case o.sem:
                f = sem
            case o.variance:
                f = functools.partial(numpy.var, ddof=1)
            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)

        self.push(f(self.take_all()))
