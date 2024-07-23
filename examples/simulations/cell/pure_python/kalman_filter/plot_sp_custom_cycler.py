import os
import pathlib
import pickle
import sys

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
# from bmslogic import cell_sim


DIR_TO_OPEN: str = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results", "sol_true_spm_discharge_kf.pkl")
with open(DIR_TO_OPEN, "rb") as pkl_file:
    sol_true: cell_sim.PySolution = pickle.load(pkl_file)

DIR_TO_OPEN: str = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results", "sol_spm_discharge_kf.pkl")
with open(DIR_TO_OPEN, "rb") as pkl_file:
    sol: cell_sim.PySolution = pickle.load(pkl_file)

DIR_TO_OPEN: str = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results", "sol_kf_spm_discharge_kf.pkl")
with open(DIR_TO_OPEN, "rb") as pkl_file:
    sol_kf: cell_sim.PySolution = pickle.load(pkl_file)


# plots
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
ax3.plot(sol.t, sol.x_surf_p, label="$SOC_{exp}$")
ax3.plot(sol_kf.t, sol_kf.x_surf_p, label="$SOC_{KF}$")
ax3.legend()

ax4 = fig.add_subplot(224)
ax4.plot(sol_true.t, sol_true.x_surf_n, label="$SOC_{true}$")
ax4.plot(sol.t, sol.x_surf_n, label="$SOC_{exp}$")
ax4.plot(sol_kf.t, sol_kf.x_surf_n, label="$SOC_{KF}$")
ax4.legend()

plt.tight_layout()
plt.legend()
plt.show()
    