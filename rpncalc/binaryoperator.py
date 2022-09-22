import numpy
import math
from rpncalc.classes import ActionEnum


class BinaryOperator(ActionEnum):

    addition = '+'
    subtraction = '-'
    multiplication = '*'
    division = '/'
    integer_division = '//'
    power = '^'
    atan2 = 'atan2', \
        "Returns quadrant correct polar coordinate theta = atan2(y,x)"
    log_base = 'log_base', \
        "Logarithm with prior arg as base" \
        "Example: 1000 10 log_base returns 3"
    equals = '='
    gt = '>'
    gte = '>='
    lt = '<'
    lte = '<='
    choose = 'choose'
    combinations = 'combo'
    modulo = '%'
    divmodulo = 'divmod', \
        "returns quotient and remainder"

    def action(self):

        v1, v0 = self.take_2()

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
            case o.integer_division:
                r = v0//v1
            case o.power:
                r = numpy.power(v0, v1)
            case o.log_base:
                r = numpy.log(v0)/numpy.log(v1)
            case o.atan2:
                r = numpy.arctan2(v0, v1)
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
                r = f(v0)//(f(v0-v1))
            case o.combinations:
                f = math.factorial
                r = f(v0)//(f(v0-v1)*f(v1))
            case o.modulo:
                r = v0 % v1
            case o.divmodulo:
                r = divmod(v0, v1)
                # divmod returns 2 valuesso push and exit
                self.push(r[0])
                self.push(r[1])
                return
            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)

        self.push(r)
