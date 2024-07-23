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
    from bmslogic.simulations.cell.solvers.battery import PyKFSPSolver
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
V_max: float = 4.2

# Modelling parameters
SOC_init_p: float = 0.4956  # from Guo et. al.
SOC_init_n: float = 0.7568  # from Guo et. al.

# Setup battery components
cell: cell_sim.PyBatteryCell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                                              soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                              temp_init=temp)

# set-up cycler and solver. The following performs simulations for the perfect condition where there are no system and sensor noises. Also, another simulation is performed
# where the simulation is performed without Kalman filter and further noise is added to the current and the voltage reading. The results from the latter simulation is later
# compared with the one where the Kalman filter is applied.
T_END: float = 4000   # [s]
TIME_INCREMENT: float = 0.2  # [s]
CURRENT_NOISE_STD: float = 0.01  # [A]
VOLTAGE_SENSOR_NOISE_STD: float = 0.01  # [V]

t: np.ndarray = np.arange(0, T_END, TIME_INCREMENT)
I_true: np.ndarray = -1.656 * np.ones(len(t))
I_noise: np.ndarray = I_true + \
    np.random.normal(loc=0.0, scale=CURRENT_NOISE_STD, size=len(I_true))

dc_true: cell_sim.PyCustomCycler = cell_sim.PyCustomCycler(
    array_t=t, array_I=I_true, V_min=V_min, V_max=V_max)
dc: cell_sim.PyCustomCycler = cell_sim.PyCustomCycler(
    array_t=t, array_I=I_noise, V_min=V_min, V_max=V_max)
solver: cell_sim.PySPSolver = cell_sim.PySPSolver(b_cell=cell,
                                                  isothermal=True, degradation=False,
                                                  electrode_SOC_solver='poly')
solver_true: cell_sim.PySPSolver = cell_sim.PySPSolver(b_cell=cell,
                                                       isothermal=True, degradation=False,
                                                       electrode_SOC_solver='poly')

# simulate
sol_true: cell_sim.PySolution = solver_true. solve(
    cycler_instance=dc_true, store_solution_iter=10)
sol: cell_sim.PySolution = solver.solve(
    cycler_instance=dc, store_solution_iter=1)
sol.V = sol.V + np.random.normal(scale=VOLTAGE_SENSOR_NOISE_STD, size=len(sol.V))

# Kalman filter simulation
cell_kf: cell_sim.PyBatteryCell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                                                 soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                                 temp_init=temp)
solver_kf: PyKFSPSolver = PyKFSPSolver(b_cell=cell_kf)
sol_kf: cell_sim.PySolution = solver_kf.solve(sol_exp=sol, cov_soc_n=1e-3, cov_soc_p=1e-3, cov_process=1e-3, cov_sensor=1e-2,
                                              v_min=2.0, v_max=4.25, soc_min=0.0, soc_max=1.0, soc_init=1.0)

# save results
DIR_TO_SAVE: str = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results", "sol_true_spm_discharge_kf.pkl")
with open(DIR_TO_SAVE, 'wb') as pkl_file:
    pickle.dump(sol_true, pkl_file, pickle.HIGHEST_PROTOCOL)

DIR_TO_SAVE = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results", "sol_spm_discharge_kf.pkl")
with open(DIR_TO_SAVE, 'wb') as pkl_file:
    pickle.dump(sol, pkl_file, pickle.HIGHEST_PROTOCOL)

DIR_TO_SAVE = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results", "sol_kf_spm_discharge_kf.pkl")
with open(DIR_TO_SAVE, 'wb') as pkl_file:
    pickle.dump(sol_kf, pkl_file, pickle.HIGHEST_PROTOCOL)

# Plot
fig = plt.figure()

ax1 = fig.add_subplot(221)
ax1.plot(sol.t, sol.V, label="$V_{terminal}$")
ax1.plot(sol_kf.t, sol_kf.V, label="KF")
ax1.legend()

ax2 = fig.add_subplot(222)
ax2.plot(sol.t, sol.I, label="$I_{true}$")
ax2.plot(sol.t, sol.I, label="$T_{exp}$")
ax2.plot()

ax3 = fig.add_subplot(223)
ax3.plot(sol_true.t, sol_true.x_surf_p, label="$SOC_{true}$")
ax3.plot(sol_kf.t, sol_kf.x_surf_p, label="$SOC_{KF}$")
ax3.plot(sol.t, sol.x_surf_p, label="$SOC_{exp}$", linestyle=":")
ax3.legend()

ax4 = fig.add_subplot(224)
ax4.plot(sol_true.t, sol_true.x_surf_n, label="$SOC_{true}$")
ax4.plot(sol.t, sol.x_surf_n, label="$SOC_{exp}$")
ax4.plot(sol_kf.t, sol_kf.x_surf_n, label="$SOC_{KF}$")
ax4.legend()

plt.tight_layout()
plt.legend()
plt.show()
