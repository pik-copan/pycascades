"""pycascades
Python framework for simulating tipping cascades on complex networks.
"""
__version__ = "1.0.2"
__author__ = 'Nico Wunderling, Jonathan Krönke, Vitus Benson, Dorothea Kistinger, Jan Kohler, Benedikt Stumpf, Valentin Wohlfarth, Jonathan F. Donges'
__credits__ = 'Potsdam Institute for Climate Impact Research'

from . import core, gen, utils, earth_system, amazon

from pycascades.core.tipping_element import cusp, hopf, realistic_cusp
from pycascades.core.tipping_element_economic import economic_logistic
from pycascades.core.tipping_network import tipping_network
from pycascades.core.tipping_network_economic import tipping_network_economic
from pycascades.core.coupling import linear_coupling, cusp_to_hopf, hopf_x_to_cusp, hopf_x_to_hopf, hopf_y_to_cusp, hopf_y_to_hopf
from pycascades.core.coupling_economic import linear_coupling as linear_coupling_economic
from pycascades.core.evolve import evolve
from pycascades.core.evolve_sde import evolve as evolve_sde
from pycascades.core.evolve_economic import evolve as evolve_economic
from pycascades.utils import plotter
