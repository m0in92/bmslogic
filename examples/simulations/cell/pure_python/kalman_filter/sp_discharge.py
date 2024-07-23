"""
This script contains the example usage of the single particle model for the discharge operation.
"""

__all__ = []

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2024 by BMSLogic. All rights reserved.'
__status__ = 'Deployed'

# try/except block are used since the user of this script can call this Python module from any file path.
# If the user calls this module from a path other than the project directory, then the except block appends the
# absolute path to the project directory to the system path.
import os
import pathlib
import pickle
import sys

import numpy as np
import matplotlib.pyplot as plt

try:
    from bmslogic import cell_sim
except ModuleNotFoundError as e:
    PROJECT_DIR: str = pathlib.Path(
        __file__).parent.parent.parent.parent.parent.parent.__str__()
    sys.path.append(PROJECT_DIR)

    from bmslogic import cell_sim
    from bmslogic.simulations.cell.solvers.battery import PyKFSPSolver

# Operating parameters
I: float = 1.656
temp: float = 298.15
V_min: float = 3.98
SOC_min: float = 0.1
soc_lib_init: float = 1.0

# Modelling parameters
SOC_init_p: float = 0.4956  # from Guo et. al.
SOC_init_n: float = 0.7568  # from Guo et. al.

# Simulation for the simulated experimental results for the Kalman filter
# Setup battery components
cell: cell_sim.PyBatteryCell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                                              soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                              temp_init=temp)

# set-up cycler and solver
dc: cell_sim.PyDischarge = cell_sim.PyDischarge(discharge_current=I, v_min=V_min,
                                                SOC_LIB_min=SOC_min, SOC_LIB=soc_lib_init)
solver: cell_sim.PySPSolver = cell_sim.PySPSolver(b_cell=cell,
                                                  isothermal=True, degradation=False,
                                                  electrode_SOC_solver='poly')

# simulate
sol: cell_sim.PySolution = solver.solve(
    cycler_instance=dc, store_solution_iter=2)
sol.V = sol.V + 0.01 * np.random.randn(len(sol.V))

# Kalman filter
cell_kf: cell_sim.PyBatteryCell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                                                 soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                                 temp_init=temp)
solver_kf: PyKFSPSolver = PyKFSPSolver(b_cell=cell_kf)
sol_kf: cell_sim.PySolution = solver_kf.solve(sol_exp=sol, cov_soc_n=1e-12, cov_soc_p=1e-12, cov_process=1e-10, cov_sensor=1e-3,
                                               v_min=2.0, v_max=4.25, soc_min=0.0, soc_max=1.0, soc_init=1.0)
# Plot
fig = plt.figure()

ax1 = fig.add_subplot(121)
ax1.plot(sol.t, sol.V, label="$V_{terminal}$")
ax1.plot(sol_kf.t, sol_kf.V, label="KF")
ax1.legend()

ax2 = fig.add_subplot(122)
ax2.plot(sol.t, sol.x_surf_n, label="$SOC_{exp}$")
ax2.plot(sol_kf.t, sol_kf.x_surf_n, label="$SOC_{KF}$")

plt.tight_layout()
plt.legend()
plt.show()
