import math

constants = {
    'pi'  : math.pi,
    'tau' : 2*math.pi,
    'c'   : 299792458,
    'h'   : 6.62607015e-34,
    'mu0' : 1.2566370621219e-6,
    'Na'  : 6.02214076e23,
    'kb'  : 1.380649e-23,
    'R'   : 8.314462618,
    'G'   : 6.6743015e-11,
    'g'   : 9.80665,
    'me'  : 9.109383701528e-31,
    'mp'  : 1.6726219236951e-27,
    'mn'  : 1.6749274980495e-27,
    }

class Constants:

    @classmethod
    def __call__(cls,arg):
        return constants[arg]

    @classmethod
    def get_names(cls):
        return tuple(constants.keys())
