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
from bmslogic.simulations.cell.cyclers import PyDischargeRest
from bmslogic.simulations.cell.solvers.electrode_conc import PyEigenFuncExp, PyCNSolver, PyPolynomialApproximation


# Electrode parameters below
R = 8.5e-6  # electrode particle radius in [m]
c_max = 51410  # max. electrode concentration [mol/m3]
D = 1e-14  # electrode diffusivity [m2/s]
S = 1.1167  # electrode electrochemical active area [m2]
SOC_init = 0.4956  # initial electrode SOC

# Simulation parameters below
i_app = 1.65  # Applied current [A]
SOC_eigen = SOC_init  # electrode current SOC
dt = 0.1  # time increment [s]
rest_time: float = 3600  # [s]

# initiate solver instances below
cn_solver: PyCNSolver = PyCNSolver(c_init=SOC_init*c_max, electrode_type='p')
eigen_solver: PyEigenFuncExp = PyEigenFuncExp(
    x_init=SOC_init, n=5, electrode_type='p')
poly_solver: PyPolynomialApproximation = PyPolynomialApproximation(
    c_init=SOC_init*c_max, electrode_type='p', type='higher')
# poly_solver_two: PyPolynomialApproximation = PyPolynomialApproximation(
#     c_init=SOC_init*c_max, electrode_type='p', type='two')

# initiate cycler instance. Note that the cyclers are programmed to be used for the battery cells and not for specific solvers.
# Hence there has to be some compromise in their usage in this script.
cycler: PyDischargeRest = PyDischargeRest(
    discharge_current=i_app, rest_time=rest_time, V_min=2.0, SOC_LIB_min=0.0, SOC_LIB=1.0, SOC_LIB_max=1.0)

# # -------------------------------------- CN Solver ---------------------------------------------------------------------

# # Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_cn_time, lst_cn_soc = [], []
t_start = time.time()  # start timer
soc_ = SOC_init
while soc_ < 0.98901:
    i_app_: float = cycler.get_current(step_name="discharge")
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
soc_ = SOC_init
while soc_ < 0.98901:
    i_app_: float = cycler.get_current(step_name="discharge")
    soc_ = eigen_solver(dt=dt, t_prev=t_prev,
                             i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_eigen_time.append(t_prev)
    lst_eigen_soc.append(soc_)
    # print(soc_)

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
while soc_ < 0.98901:
    i_app_: float = cycler.get_current(step_name="discharge")
    soc_ = poly_solver(dt=dt, t_prev=t_prev,
                           i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_poly_time.append(t_prev)
    lst_poly_soc.append(soc_)

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

with open(os.path.join(FILE_DIR, "saved_results", "pos_discharge_rest_cn_time.pkl"), "wb") as pkl_cn_file:
    pickle.dump(lst_cn_time, pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_discharge_rest_cn_soc.pkl"), "wb") as pkl_cn_file:
    pickle.dump(lst_cn_soc, pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_discharge_rest_eigen_time.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_time, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_discharge_rest_eigen_soc.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_soc, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_discharge_rest_poly_time.pkl"), "wb") as pkl_poly_file:
    pickle.dump(lst_poly_time, pkl_poly_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_discharge_rest_poly_soc.pkl"), "wb") as pkl_poly_file:
    pickle.dump(lst_poly_soc, pkl_poly_file)

# --------------------------------PLOTS-----------------------------------------------------------
plt.plot(lst_cn_time, lst_cn_soc, label="CN")
plt.plot(lst_eigen_time, lst_eigen_soc, label="eigen")
plt.plot(lst_poly_time, lst_poly_soc, label="poly-higher")
# plt.plot(lst_poly_two_time, lst_poly_two_soc, label="poly-two")

plt.legend()
plt.show()
