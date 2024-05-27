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
V_min: float = 3
V_max: float = 4.2
SOC_min: float = 0.1
soc_lib_init: float = 1.0
rest_time: float = 3600  # [s]
SOC_LIB_MAX: float = 1

# Modelling parameters
soc_init_p: float = 0.989011
soc_init_n: float = 0.01890232

# Setup battery components
cell: cell_sim.PyBatteryCell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                                              soc_init_p=soc_init_p, soc_init_n=soc_init_n,
                                                                              temp_init=temp)

# set-up cycler and solver
dc: cell_sim.PyDischargeRest = cell_sim.PyChargeRest(charge_current=I, rest_time=rest_time, 
                                                     V_max=V_max,
                                                     SOC_LIB=soc_lib_init, SOC_LIB_max=SOC_LIB_MAX)
solver: cell_sim.PySPSolver = cell_sim.PySPSolver(b_cell=cell,
                                                  isothermal=False, degradation=False,
                                                  electrode_SOC_solver='poly')

# simulate
sol = solver.solve(cycler_instance=dc)

# save_results
DIR_TO_SAVE: str = os.path.join(pathlib.Path(
    __file__).parent.__str__(), "saved_results")

with open(os.path.join(DIR_TO_SAVE, "charge_rest_spm_isothermal_time.pkl"), "wb") as pkl_file:
    pickle.dump(sol.t.tolist(), pkl_file)

with open(os.path.join(DIR_TO_SAVE, "charge_rest_spm_isothermal_V.pkl"), "wb") as pkl_file:
    pickle.dump(sol.V.tolist(), pkl_file)

# Plot
fig = plt.figure(figsize=(10, 3), dpi=300)
ax1 = fig.add_subplot(121)
ax1.plot(sol.t, sol.I)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Current [A]')

ax2 = fig.add_subplot(122)
ax2.plot(sol.t, sol.V, label="Polynomial Approximation", linewidth=2)
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Cell Terminal Voltage [V]')

plt.tight_layout()
plt.show()
