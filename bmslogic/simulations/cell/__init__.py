"""
Package header for the bmslogic.simulations.cell namespace
Provides the continuum scale battery cell simulations.
"""

__all__ = ['battery_components', 'calc_helpers', 'config', 'cycler', 'general_OCP', 'models',
           'parameter_estimations', 'solvers', 'sol_and_visualization', 'warnings_and_exceptions']

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2024 by BMSLogic. All rights are reserved.'
__status__ = 'Deployed'

import bmslogic.simulations.cell.general_ocps as general_ocps
from bmslogic.simulations.cell.battery_components import PyElectrode, PyNElectrode, PyPElectrode, PyBatteryCell, PyECMBatteryCell, PyElectrolyte

from bmslogic.simulations.cell.cyclers import PyCharge, PyChargeRest, PyDischarge, PyDischargeRest, PyCustomDischarge, PyCustomCycler, PyHPPCCycler

from bmslogic.simulations.cell.solution import PySolution, PyECMSolution

from bmslogic.simulations.cell.solvers.battery import PySPSolver, PyEnhancedSPSolver

# CPP from pybind11
# from cell import ElectrolyteFVMCoordinates, ElectrolyteFVMSolver