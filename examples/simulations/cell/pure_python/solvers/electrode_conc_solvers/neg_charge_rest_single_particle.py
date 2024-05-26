"""
Contains the script for comparing the solvers for the lithium diffusivity in the solid electrode region under
the battery cell discharge rest.
"""
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."

import pathlib
import pickle  # pickle is used for storing the results of this script
import os
import sys
import time

import matplotlib.pyplot as plt

sys.path.append(pathlib.Path(
    __file__).parent.parent.parent.parent.parent.parent.parent.__str__())
from bmslogic.simulations.cell.solvers.electrode_conc import PyEigenFuncExp, PyCNSolver, PyPolynomialApproximation
from bmslogic.simulations.cell.cyclers import PyChargeRest


# Electrode parameters below
R = 1.25e-5  # electrode particle radius in [m]
c_max = 31833  # max. electrode concentration [mol/m3]
D = 3.9e-14  # electrode diffusivity [m2/s]
S = 0.7824  # electrode electrochemical active area [m2]
SOC_init = 0.0189023  # initial electrode SOC

# Simulation parameters below
i_app = 1.65  # Applied current [A]
SOC_eigen = SOC_init  # electrode current SOC
dt = 0.1  # time increment [s]
rest_time: float = 3600  # [s]

# initiate solver instances below
eigen_solver: PyEigenFuncExp = PyEigenFuncExp(
    x_init=SOC_init, n=5, electrode_type='n')
cn_solver: PyCNSolver = PyCNSolver(c_init=SOC_init*c_max, electrode_type='n')
poly_solver: PyPolynomialApproximation = PyPolynomialApproximation(
    c_init=SOC_init*c_max, electrode_type='n', type='higher')

# initiate cycler instance. Note that the cyclers are programmed to be used for the battery cells and not for specific solvers.
# Hence there has to be some compromise in their usage in this script.
cycler: PyChargeRest = PyChargeRest(
    charge_current=i_app, rest_time=rest_time, V_max=4.2)

# # -------------------------------------- CN Solver ---------------------------------------------------------------------

# # Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_cn_time, lst_cn_soc = [], []
t_start = time.time()  # start timer
soc_ = SOC_init
while soc_ < 0.7568:
    i_app_: float = cycler.get_current(step_name="charge")
    soc_ = cn_solver(dt=dt, t_prev=t_prev, i_app=i_app_,
                     R=R, S=S, D_s=D, c_smax=c_max, solver_method="TDMA")
    lst_cn_time.append(t_prev)
    lst_cn_soc.append(soc_)

    t_prev += dt  # update the time

while cycler.time_elapsed < rest_time:
    i_app_ = cycler.get_current(step_name="rest")
    soc_ = cn_solver(dt=dt, t_prev=t_prev,
                     i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_cn_time.append(t_prev)
    lst_cn_soc.append(soc_)

    cycler.time_elapsed += dt
    t_prev += dt  # update the time
    # print(cycler.time_elapsed)
t_end = time.time()  # end timer
cycler.reset()
print(f"CN solver solved in {t_end - t_start} s")

# ----------------------------------EIGEN SOLVER------------------------------------------------------------------------

t_prev: float = 0.0  # previous time [s]

# solve for SOC wrt to time
lst_eigen_time, lst_eigen_soc = [], []
t_start = time.time()  # start timer
soc_: float = SOC_init
while soc_ < 0.7568:
    i_app_: float = cycler.get_current(step_name="charge")
    soc_ = eigen_solver(dt=dt, t_prev=t_prev,
                             i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_eigen_time.append(t_prev)
    lst_eigen_soc.append(soc_)

    t_prev += dt  # update the time

while cycler.time_elapsed < rest_time:
    i_app_ = cycler.get_current(step_name="rest")
    soc_ = eigen_solver(dt=dt, t_prev=t_prev,
                        i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_eigen_time.append(t_prev)
    lst_eigen_soc.append(soc_)

    cycler.time_elapsed += dt
    t_prev += dt  # update the time
    # print(cycler.time_elapsed)
t_end = time.time()  # end timer
cycler.reset()
print(f"eigen solver solved in {t_end - t_start} s")

# -------------------------------------- POLYSOLVER  - HIGHER ORDER -------------------------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_poly_time, lst_poly_soc = [], []
t_start = time.time()  # start timer
soc_ = SOC_init
while soc_ < 0.7568:
    i_app_: float = cycler.get_current(step_name="charge")
    soc_ = poly_solver(dt=dt, t_prev=t_prev,
                       i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_poly_time.append(t_prev)
    lst_poly_soc.append(soc_)
    # print(soc_)

    t_prev += dt  # update the time

while cycler.time_elapsed < rest_time:
    i_app_ = cycler.get_current(step_name="rest")
    soc_ = poly_solver(dt=dt, t_prev=t_prev,
                i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_poly_time.append(t_prev)
    lst_poly_soc.append(soc_)

    cycler.time_elapsed += dt
    t_prev += dt  # update the time
    # print(cycler.time_elapsed)

t_end = time.time()  # end timer
cycler.reset()
print(f"Poly solver solved in {t_end - t_start} s")

# ----------------------------------------------Save Results-----------------------------------------------------------

FILE_DIR: str = pathlib.Path(__file__).parent.__str__()

with open(os.path.join(FILE_DIR, "saved_results", "neg_charge_rest_cn_time.pkl"), "wb") as pkl_cn_file:
    pickle.dump(lst_cn_time, pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "neg_charge_rest_cn_soc.pkl"), "wb") as pkl_cn_file:
    pickle.dump(lst_cn_soc, pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "neg_charge_rest_eigen_time.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_time, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "neg_charge_rest_eigen_soc.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_soc, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "neg_charge_rest_poly_time.pkl"), "wb") as pkl_poly_file:
    pickle.dump(lst_poly_time, pkl_poly_file)

with open(os.path.join(FILE_DIR, "saved_results", "neg_charge_rest_poly_soc.pkl"), "wb") as pkl_poly_file:
    pickle.dump(lst_poly_soc, pkl_poly_file)

# --------------------------------PLOTS-----------------------------------------------------------
plt.plot(lst_cn_time, lst_cn_soc, label="CN")
plt.plot(lst_eigen_time, lst_eigen_soc, label="eigen")
plt.plot(lst_poly_time, lst_poly_soc, label="poly-higher")

plt.legend()
plt.show()
