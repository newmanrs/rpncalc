import math
from rpncalc.classes import ActionEnum


class Constant(ActionEnum):

    def __init__(self, value, constant_value=None, description=None):
        self.constant_value = constant_value
        self.description = description

    def help(self):
        msg = f" Constant {self.value} is {self.constant_value}."
        msg += super().help()
        return msg

    true = "true", 1, "Alias for 1"
    false = "false", 0, "Alias for 0"
    pi = "pi", math.pi, "Value of pi"
    tau = "tau", 2*math.pi, "Value of 2pi"
    ln_base = (
        "e",
        math.e,
        "Natural logarithm base")
    lightspeed = "c", 299792458, "Speed of light, (m/s)"
    planck = "h", 6.62607015e-34, "Planck's constant (m^2/kg/s)"
    permittivity = "mu0",  1.2566370621219e-6, \
        "permittivity of free space (F/m)"
    avogadro = "Na", 6.02214076e23, "Avogadro's Number"
    boltzmann = "kb", 1.380649e-23, "Boltzmann Constant (J/K)"
    gas_constant = "R", 8.314462618, "Ideal gas constant, (J/molK)"
    gravitational_constant = "G", 6.6743015e-11, \
        "Gravitational Constant"
    earth_gravity_acc = "g", 9.80665, "Earth mean acceleration (m/s^2)"
    mass_electron = "m_e", 9.109383701528e-31, "Electron Mass (kg)"
    mass_proton = "m_p", 1.6726219236951e-27, "Proton Mass (kg)"
    mass_neutron = "m_n", 1.6749274980495e-27, "Neutron Mass (kg)"

    def action(self):
        self.push(self.constant_value)
