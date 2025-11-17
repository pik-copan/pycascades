"""pycascades
Python framework for simulating tipping cascades on complex networks.
"""
__version__ = "1.0.2"
__author__ = 'Nico Wunderling, Jonathan Krönke, Vitus Benson, Dorothea Kistinger, Jan Kohler, Benedikt Stumpf, Valentin Wohlfarth, Jonathan F. Donges'
__credits__ = 'Potsdam Institute for Climate Impact Research'

from . import core, gen, utils, earth_system, amazon

from pycascades.core.coupling import linear_coupling
from pycascades.core.evolve import evolve
from pycascades.utils import plotter
