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
matplotlib.rc('xtick', labelsize=12) 
matplotlib.rc('ytick', labelsize=12) 

plt.plot(sol.t, sol.I, label=r"$I_{noisy}$", linestyle=":")
plt.plot(sol_true.t, sol_true.I, label=r"$I_{true}$")

plt.xlabel("Time [$s$]", fontsize=15)
plt.ylabel("Applied Current [$A$]", fontsize=15)

plt.legend(fontsize=12)
plt.tight_layout()
plt.show()
