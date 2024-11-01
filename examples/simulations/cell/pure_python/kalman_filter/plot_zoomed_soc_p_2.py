import os
import pathlib
import pickle
import sys

import matplotlib
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


DIR_TO_OPEN: str = os.path.join(pathlib.Path(
    __file__).parent.__str__(), "saved_results", "sol_true_spm_discharge_kf.pkl")
with open(DIR_TO_OPEN, "rb") as pkl_file:
    sol_true: cell_sim.PySolution = pickle.load(pkl_file)

DIR_TO_OPEN: str = os.path.join(pathlib.Path(
    __file__).parent.__str__(), "saved_results", "sol_spm_discharge_kf.pkl")
with open(DIR_TO_OPEN, "rb") as pkl_file:
    sol: cell_sim.PySolution = pickle.load(pkl_file)

DIR_TO_OPEN: str = os.path.join(pathlib.Path(
    __file__).parent.__str__(), "saved_results", "sol_kf_spm_discharge_kf.pkl")
with open(DIR_TO_OPEN, "rb") as pkl_file:
    sol_kf: cell_sim.PySolution = pickle.load(pkl_file)


# plots
matplotlib.rc('xtick', labelsize=25)
matplotlib.rc('ytick', labelsize=25)

plt.plot(sol.t, sol.x_surf_p, label=r"$SOC_{p,noisy}$", linewidth=3)
plt.plot(sol_kf.t, sol_kf.x_surf_p, label=r"$SOC_{p,SPKF}$", linewidth=3)
plt.plot(sol_true.t, sol_true.x_surf_p,
         label=r"$SOC_{p,true}$", linestyle=":", linewidth=3)

plt.xlim(3000, 4100)
plt.ylim(0.85, 1)
plt.tight_layout()
plt.show()
