import math
from rpncalc.util import ActionEnum


class Constant(ActionEnum):

    def __init__(self, value, constant_value=None, description=None):
        self.constant_value = constant_value
        self.description = description

    def help(self):
        msg = f"Constant {self.value} is {self.constant_value}."
        if self.description:
            msg += f" {self.description}."
        return msg

    pi = 'pi', math.pi, "Value of pi"
    tau = 'tau', 2*math.pi, "Value of 2pi"
    ln_base = (
        'e',
        math.e,
        "Natural logarithm base")
    lightspeed = 'c', 299792458, "Speed of light"
    planck = 'h', 6.62607015e-34, "Planck's constant"
    permittivity = 'mu0',  1.2566370621219e-6, \
        "permittivity of free space"
    avogadro = 'Na', 6.02214076e23
    boltzmann = 'kb', 1.380649e-23
    gas_constant = 'R', 8.314462618
    gravitational_constant = 'G', 6.6743015e-11
    earth_gravity_acc = 'g', 9.80665
    mass_electron = 'me', 9.109383701528e-31
    mass_proton = 'mp', 1.6726219236951e-27
    mass_neutron = 'mn', 1.6749274980495e-27

    def action(self):
        self.push(self.constant_value)
