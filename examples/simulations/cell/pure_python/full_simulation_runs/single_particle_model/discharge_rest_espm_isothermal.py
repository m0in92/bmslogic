"""
Contains the example implementation of SPPy using a discharge and rest operation under
isothermal conditions.
"""
__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by SPPy. All rights reserved.'
__status__ = 'deployed'


# try/except block are used since the user of this script can call this Python module from any file path.
# If the user calls this module from a path other than the project directory, then the except block appends the
# absolute path to the project directory to the system path.
import os
import pathlib
import pickle
import sys

import matplotlib.pyplot as plt

try:
    from bmslogic import cell_sim
except ModuleNotFoundError as e:
    PROJECT_DIR: str = pathlib.Path(
        __file__).parent.parent.parent.parent.parent.parent.parent.__str__()
    sys.path.append(PROJECT_DIR)

    from bmslogic import cell_sim

"""
This script contains the example usage of the single particle model for the discharge operation under non-isothermal conditions.
"""

__all__ = []

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2024 by BMSLogic. All rights reserved.'
__status__ = 'Deployed'


# Operating parameters
I: float = 1.656
temp: float = 298.15
V_min: float = 2.5  # in V
SOC_min: float = 0.1
soc_lib_init: float = 1.0
rest_time: float = 500  # [s]
SOC_LIB_MAX: float = 1

# Modelling parameters
SOC_init_p: float = 0.4956  # from Guo et. al.
SOC_init_n: float = 0.7568  # from Guo et. al.

# Setup battery components
cell: cell_sim.PyBatteryCell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                                              soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                              temp_init=temp)


# set-up cycler and solver
cycler: cell_sim.PyDischargeRest = cell_sim.PyDischargeRest(discharge_current=I, V_min=V_min,
                                                            SOC_LIB_min=SOC_min, SOC_LIB=soc_lib_init,
                                                            rest_time=rest_time, SOC_LIB_max=SOC_LIB_MAX)
solver: cell_sim.PyEnhancedSPSolver = cell_sim.PyEnhancedSPSolver(b_cell=cell, electrode_soc_solver="poly",
                                                                  isothermal=True, degradation=False)

# simulate
sol: cell_sim.PySolution = solver.solve(cycler=cycler, verbose=False)

# save_results
DIR_TO_SAVE: str = os.path.join(pathlib.Path(
    __file__).parent.__str__(), "saved_results")

with open(os.path.join(DIR_TO_SAVE, "discharge_rest_espm_isothermal_time.pkl"), "wb") as pkl_file:
    pickle.dump(sol.t.tolist(), pkl_file)

with open(os.path.join(DIR_TO_SAVE, "discharge_rest_espm_isothermal_V.pkl"), "wb") as pkl_file:
    pickle.dump(sol.V.tolist(), pkl_file)

# Plot
sol.comprehensive_isothermal_plot()
# fig = plt.figure(figsize=(10, 3), dpi=300)
# ax1 = fig.add_subplot(121)
# ax1.plot(sol.t, sol.I)
# ax1.set_xlabel('Time [s]')
# ax1.set_ylabel('Current [A]')

# ax2 = fig.add_subplot(122)
# ax2.plot(sol.t, sol.V, label="Polynomial Approximation", linewidth=2)
# ax2.set_xlabel('Time [s]')
# ax2.set_ylabel('Cell Terminal Voltage [V]')

# plt.tight_layout()
# plt.show()
