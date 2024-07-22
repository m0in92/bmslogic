"""
This module is an example implementation of cell_simCPPy using the NElectrode, PElectrode, Electrolyte, and BatteryCell class.
"""

__author__ = "Moin Ahmed"
__copyright__ = 'Copyright 2024 by BMSLogic. All rights reserved.'
__status__ = 'Developement'

import time
import os
import pathlib
import pickle
import sys

import numpy as np
import matplotlib.pyplot as plt

try:
    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    from bmslogic.simulations.cell.plot import Plot

    from examples.simulations.cell.example_parameter import *

except ModuleNotFoundError as e:
    PROJECT_DIR: str = pathlib.Path(
        __file__).parent.parent.parent.parent.__str__()
    print(PROJECT_DIR)
    sys.path.append(PROJECT_DIR)

    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    from bmslogic.simulations.cell.plot import Plot

    from examples.simulations.cell.example_parameter import *


SOC_init_p: float = 0.4952
SOC_init_n: float = 0.7522

cycler_time: np.ndarray = np.arange(0, 6000, 0.1)
cycler_current: np.ndarray = np.zeros(len(cycler_time))

battery_cell: cell_sim.BatteryCell = ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
                                                                                              soc_p_init=SOC_init_p,
                                                                                              T_amb=T,
                                                                                              R_cell=R_cell)

cycler: cell_sim.HPPCCycler = cell_sim.HPPCCycler(
    t1=500, t2=100, i_app=1.5, n_hppc_steps=1000, V_min=3.0, soc_lib_min=0.0, soc_lib=1.0)

# print(cycler.get_current("discharge", 501.0))

# for i in range(len(cycler_current)):
#     cycler_current[i] = cycler.get_current("asdf", cycler_time[i])

solver: cell_sim.BatterySolver = cell_sim.BatterySolver(battery_cell=battery_cell,
                                                        is_isothermal=True,
                                                        enable_degradation=False)
sol: cell_sim.Solution = solver.solve(cycler=cycler)

# plots
# Plot(sol=sol).plot_comprehensive()

plt.plot(cycler_time, cycler_current)

# plt.ylim(-2, 1)
plt.show()
