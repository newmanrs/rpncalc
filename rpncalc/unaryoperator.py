import numpy
import math
from rpncalc.classes import ActionEnum


def expmxsq(x):
    return numpy.exp(-(x*x))


def inv(x):
    return 1.0/x


def uminus(x):
    return -x


class UnaryOperator(ActionEnum):

    sin = 'sin'
    cos = 'cos'
    tan = 'tan'
    acos = 'acos'
    asin = 'asin'
    atan = 'atan'
    to_int = 'int'
    exp = 'exp'
    expmxsq = 'expmxsq', \
        "computes exp(-x^2)"
    fact = '!'
    ln = 'ln'
    log10 = 'log10'
    sqrt = 'sqrt'
    inverse = '1/x'
    uminus = 'uminus'

    def action(self):

        x = self.take_1()

        o = type(self)
        match self:

            case o.sin:
                f = numpy.sin
            case o.cos:
                f = numpy.cos
            case o.tan:
                f = numpy.tan
            case o.asin:
                f = numpy.arcsin
            case o.exp:
                f = numpy.exp
            case o.ln:
                f = numpy.log
            case o.log10:
                f = numpy.log10
            case o.expmxsq:
                f = expmxsq
            case o.fact:
                f = math.factorial
            case o.acos:
                f = numpy.arccos
            case o.atan:
                f = numpy.arctan
            case o.sqrt:
                f = numpy.sqrt
            case o.to_int:
                f = int
            case o.inverse:
                f = inv
            case o.uminus:
                f = uminus
            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)

        self.push(f(x))
