import numpy
from rpncalc.classes import ActionEnum

rng = numpy.random.default_rng()


class RandomOperator(ActionEnum):

    rand = 'rand', "Random double on [0,1)"
    coin = 'coin', "Random fair coinflip from {0,1}"
    d2 = 'd2', "Roll two-sided die (1,2)"
    d4 = 'd4', "Roll die (1, 2, .., 4)"
    d6 = 'd6', "Roll die (1, 2, .., 6)"
    d8 = 'd8', "Roll die (1, 2, .., 8)"
    d10 = 'd10', "Roll die (1, 2, .., 10)"
    d12 = 'd12', "Roll die (1, 2, .., 12)"
    d20 = 'd20', "Roll die (1, 2, .., 20)"
    d100 = 'd100', "Roll die (1, 2, .., 100)"

    def action(self):

        o = type(self)

        match self:
            case o.rand:
                roll = rng.random()
            case o.coin:
                roll = rng.integers(2)
            case o.d2:
                roll = rng.integers(1, 2, endpoint=True)
            case o.d4:
                roll = rng.integers(1, 4, endpoint=True)
            case o.d6:
                roll = rng.integers(1, 6, endpoint=True)
            case o.d8:
                roll = rng.integers(1, 8, endpoint=True)
            case o.d12:
                roll = rng.integers(1, 12, endpoint=True)
            case o.d20:
                roll = rng.integers(1, 20, endpoint=True)
            case o.d100:
                roll = rng.integers(1, 100, endpoint=True)
            case _:
                msg = f"Missing case match for action {self}"
                raise NotImplementedError(msg)

        self.push(roll)
