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

import numpy as np
import matplotlib.pyplot as plt

sys.path.append(pathlib.Path(
    __file__).parent.parent.parent.parent.parent.parent.parent.__str__())
from bmslogic.simulations.cell.cyclers import PyDischarge
from bmslogic.simulations.cell.solvers.electrode_conc import PyCNSolver


# Electrode parameters below
R = 1.25e-5  # electrode particle radius in [m]
c_max = 31833  # max. electrode concentration [mol/m3]
D = 3.9e-14  # electrode diffusivity [m2/s]
S = 0.7824  # electrode electrochemical active area [m2]
SOC_init = 0.7568  # initial electrode SOC

# Simulation parameters below
i_app = 1.65  # Applied current [A]
SOC_eigen = SOC_init  # electrode current SOC
dt = 0.1  # time increment [s]

# initiate solver instances below
cn_solver_inverse: PyCNSolver = PyCNSolver(
    c_init=SOC_init*c_max, electrode_type='n')
cn_solver_TDMA: PyCNSolver = PyCNSolver(
    c_init=SOC_init*c_max, electrode_type='n')

# initiate cycler instance. Note that the cyclers are programmed to be used for the battery cells and not for specific solvers.
# Hence there has to be some compromise in their usage in this script.
cycler: PyDischarge = PyDischarge(
    discharge_current=i_app, v_min=2.0, SOC_LIB_min=0.0, SOC_LIB=1.0)

# ---------------------------------------SIMULATion FUNCTIONS ----------------------------------------------------------

def matprint(mat: np.ndarray, fmt: str="g") -> None:
    col_maxes = [max([len(("{:"+fmt+"}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:"+str(col_maxes[i])+fmt+"}").format(y), end="  ")
        print("")


def perform_cn_sim(soc_init: float, cn_method_type: str) -> tuple[list, list]:
    """Simple function to perform the simulation on the global parameters above

    Args:
        soc_init (float): electrode initial soc
        cn_method_type (str): "inverse" or "TDMA"

    Raises:
        ValueError: if the method type is not supported

    Returns:
        tuple[list, list]: list containing the simulation time and soc.
    """

    if (cn_method_type != "inverse") and (cn_method_type != "TDMA"):
        raise ValueError(f"invalid CN method type: {cn_method_type}.")

    # initiate solver instances below
    cn_solver: PyCNSolver = PyCNSolver(
        c_init=SOC_init*c_max, electrode_type='n')
    
    # print(matprint(cn_solver.M(dt=dt, R=R, D=D)))
    print(cn_solver.M(dt=dt, R=R, D=D))

    # # Simulation parameters below
    t_prev = 0  # previous time [s]

    # solve for SOC wrt to time
    lst_time, lst_soc = [], []
    t_start = time.time()  # start timer
    soc_ = SOC_init
    while soc_ > 0:
        i_app_: float = cycler.get_current(step_name="discharge")
        soc_ = cn_solver(dt=dt, t_prev=t_prev, i_app=i_app_,
                            R=R, S=S, D_s=D, c_smax=c_max, solver_method=cn_method_type)
        lst_time.append(t_prev)
        lst_soc.append(soc_)

        t_prev += dt  # update the time
    t_end = time.time()  # end timer
    print(f"CN solver solved in {t_end - t_start} s")

    return lst_time, lst_soc

# # -------------------------------------- SIMULATION RUN ---------------------------------------------------------------------
N_SIM: int = 5

for i in range(N_SIM):
    lst_time_inverse, lst_soc_inverse = perform_cn_sim(soc_init=SOC_init, cn_method_type="inverse")
    lst_time_TDMA, lst_soc_TDMA = perform_cn_sim(soc_init=SOC_init, cn_method_type="TDMA")

# Save Results
FILE_DIR: str = pathlib.Path(__file__).parent.__str__()

with open(os.path.join(FILE_DIR, "saved_results", "cn_neg_discharge_inverse_time.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_time_inverse, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "cn_neg_discharge_inverse_soc.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_soc_inverse, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "cn_neg_discharge_TDMA_time.pkl"), "wb") as pkl_cn_file:
    pickle.dump(lst_time_TDMA, pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "cn_neg_discharge_TDMA_soc.pkl"), "wb") as pkl_cn_file:
    pickle.dump(lst_soc_TDMA, pkl_cn_file)

# plots
plt.plot(lst_time_inverse, lst_soc_inverse)
plt.plot(lst_time_TDMA, lst_soc_TDMA)

plt.show()
