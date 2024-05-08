"""
This script contains the example usage of the single particle model in the charge operation. The degradation mode used
if the reduced-order SEI model.
"""

__all__ = []

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2024 by BMSLogic. All Rights Reserved.'
__status__ = 'Deployed'

import matplotlib.pyplot as plt

from bmslogic import cell_sim

# Operating parameters
I: float = 1.656
T: float = 298.15
V_max: float = 4.2
SOC_max: float = 0.9
SOC_LIB: float = 0.9

# Modelling parameters
SOC_init_p: float = 0.989011
SOC_init_n: float = 0.01890232

# Setup battery components
cell: cell_sim.PyBatteryCell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                                              soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                              temp_init=T)

# set-up cycler and solver
dc: cell_sim.PyCharge = cell_sim.PyCharge(
    charge_current=I, V_max=V_max, SOC_LIB_max=SOC_max, SOC_LIB=SOC_LIB)
solver: cell_sim.PySPSolver = cell_sim.PySPSolver(b_cell=cell, isothermal=True, degradation=True,
                                                  electrode_SOC_solver='poly')

# simulate
sol: cell_sim.PySolution = solver.solve(cycler_instance=dc)

# Plot
sol.plot_degradation()
