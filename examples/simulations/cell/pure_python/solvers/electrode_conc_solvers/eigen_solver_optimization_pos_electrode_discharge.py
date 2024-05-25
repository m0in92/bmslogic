"""
Contains the script for comparing the solvers for the lithium diffusivity in the solid electrode region.
"""
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."

import pathlib
import pickle  # pickle is used for storing the results of this script
import os
import sys
import time

# from memory_profiler import profile
import matplotlib.pyplot as plt

sys.path.append(pathlib.Path(
    __file__).parent.parent.parent.parent.parent.parent.parent.__str__())
from bmslogic.simulations.cell.cyclers import PyDischarge
from bmslogic.simulations.cell.solvers.electrode_conc import PyEigenFuncExp


# Electrode parameters below
R = 8.50E-06  # electrode particle radius in [m]
c_max = 51410 # max. electrode concentration [mol/m3]
D = 1.00E-14  # electrode diffusivity [m2/s]
S = 1.1167  # electrode electrochemical active area [m2]
SOC_init = 0.4956  # initial electrode SOC

# initiate solver instances below
eigen_solver_2: PyEigenFuncExp = PyEigenFuncExp(
    x_init=SOC_init, n=2, electrode_type='p')
eigen_solver_5: PyEigenFuncExp = PyEigenFuncExp(
    x_init=SOC_init, n=5, electrode_type='p')
eigen_solver_10: PyEigenFuncExp = PyEigenFuncExp(
    x_init=SOC_init, n=10, electrode_type='p')
eigen_solver_20: PyEigenFuncExp = PyEigenFuncExp(
    x_init=SOC_init, n=20, electrode_type='p')
eigen_solver_25: PyEigenFuncExp = PyEigenFuncExp(
    x_init=SOC_init, n=25, electrode_type='p')

# Simulation parameters below
i_app = -1.65  # Applied current [A]
dt = 0.1  # time increment [s]

# initiate cycler instance. Note that the cyclers are programmed to be used for the battery cells and not for specific solvers.
# Hence there has to be some compromise in their usage in this script.
cycler: PyDischarge = PyDischarge(
    discharge_current=i_app, v_min=2.0, SOC_LIB_min=0.0, SOC_LIB=1.0)


def perform_eigen_discharge_sim(soc_init: float, N: int) -> tuple[list, list]:
    """function to perform the Eigen Expansion Method of the negative electrode during battery discharge.

    Args:
        soc_init (float): the initial electrode SOC
        N (int): the number roots of the Eigen Functions

    Returns:
       tuple[list, list]: tuple vontaining lists of the solution time elapsed and the electode SOC
    """
    eigen_solver: PyEigenFuncExp = PyEigenFuncExp(
        x_init=soc_init, n=N, electrode_type='n')

    t_prev: float = 0.0  # previous time [s]
    eigen_soc_ = soc_init  # electrode current SOC

    # solve for SOC wrt to time
    lst_eigen_time, lst_eigen_soc = [], []
    t_start = time.time()  # start timer
    while eigen_soc_ < 0.98901:
        i_app_: float = cycler.get_current(step_name="discharge")
        eigen_soc_ = eigen_solver(
            dt=dt, t_prev=t_prev, i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
        lst_eigen_time.append(t_prev)
        lst_eigen_soc.append(eigen_soc_)

        t_prev += dt  # update the time
    t_end = time.time()  # end timer
    print(f"eigen solver -N={N}- solved in {t_end - t_start} s")

    return lst_eigen_time, lst_eigen_soc


# ----------------------------------Simulations------------------------------------------------------------------------
n_sim: int = 5  # number of simulation runs

for i in range(n_sim):
    lst_eigen_time_2, lst_eigen_soc_2 = perform_eigen_discharge_sim(
        soc_init=SOC_init, N=2)
    lst_eigen_time_5, lst_eigen_soc_5 = perform_eigen_discharge_sim(
        soc_init=SOC_init, N=5)
    lst_eigen_time_10, lst_eigen_soc_10 = perform_eigen_discharge_sim(soc_init=SOC_init, N=10)
    lst_eigen_time_20, lst_eigen_soc_20 = perform_eigen_discharge_sim(soc_init=SOC_init, N=20)
    lst_eigen_time_50, lst_eigen_soc_50 = perform_eigen_discharge_sim(soc_init=SOC_init, N=50)
    lst_eigen_time_100, lst_eigen_soc_100 = perform_eigen_discharge_sim(soc_init=SOC_init, N=100)

# -------------------------------------save the results --------------------------------------------------------

FILE_DIR: str = pathlib.Path(__file__).parent.__str__()

# N=2
with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_time_2.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_time_2, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_soc_2.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_soc_2, pkl_eigen_file)

# N=5
with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_time_5.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_time_5, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_soc_5.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_soc_5, pkl_eigen_file)

# N=10
with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_time_10.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_time_10, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_soc_10.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_soc_10, pkl_eigen_file)

# N=20
with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_time_20.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_time_20, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_soc_20.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_soc_20, pkl_eigen_file)

# N=50
with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_time_50.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_time_50, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_soc_50.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_soc_50, pkl_eigen_file)

# N=100
with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_time_100.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_time_100, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_soc_100.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_soc_100, pkl_eigen_file)

# ----------------------------------Plots ------------------------------------------------------------------------
plt.plot(lst_eigen_time_2, lst_eigen_soc_2, label="N=2")
plt.plot(lst_eigen_time_5, lst_eigen_soc_5, label="N=5")
plt.plot(lst_eigen_time_10, lst_eigen_soc_10, label="N=10")
plt.plot(lst_eigen_time_20, lst_eigen_soc_20, label="N=20")
plt.plot(lst_eigen_time_50, lst_eigen_soc_50, label="N=50")
plt.plot(lst_eigen_time_100, lst_eigen_soc_100, label="N=100")

plt.legend()
plt.show()
