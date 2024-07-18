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

import matplotlib.pyplot as plt

sys.path.append(pathlib.Path(
    __file__).parent.parent.parent.parent.parent.parent.parent.__str__())

from bmslogic.simulations.cell.cyclers import PyDischarge
from bmslogic.simulations.cell.solvers.electrode_conc import PyEigenFuncExp, PyCNSolver, PyPolynomialApproximation


# Electrode parameters below
R = 1.25e-5  # electrode particle radius in [m]
c_max = 31833  # max. electrode concentration [mol/m3]
D = 3.9e-14  # electrode diffusivity [m2/s]
S = 0.7824  # electrode electrochemical active area [m2]
SOC_init = 0.7568  # initial electrode SOC

# initiate solver instances below
eigen_solver: PyEigenFuncExp = PyEigenFuncExp(
    x_init=SOC_init, n=5, electrode_type='n')
cn_solver: PyCNSolver = PyCNSolver(c_init=SOC_init*c_max, electrode_type='n')
poly_solver: PyPolynomialApproximation = PyPolynomialApproximation(
    c_init=SOC_init*c_max, electrode_type='n', type='higher')
poly_solver_two: PyPolynomialApproximation = PyPolynomialApproximation(
    c_init=SOC_init*c_max, electrode_type='n', type='two')

# Simulation parameters below
i_app = 1.65  # Applied current [A]
SOC_eigen = SOC_init  # electrode current SOC
dt = 0.1  # time increment [s]

# initiate cycler instance. Note that the cyclers are programmed to be used for the battery cells and not for specific solvers.
# Hence there has to be some compromise in their usage in this script.
cycler: PyDischarge = PyDischarge(
    discharge_current=i_app, v_min=2.0, SOC_LIB_min=0.0, SOC_LIB=1.0)

# # -------------------------------------- CN Solver ---------------------------------------------------------------------

# # Simulation parameters below
t_prev = 0  # previous time [s]

print(cn_solver.c_prev[-1])
i_app_: float = cycler.get_current(step_name="discharge")
SOC_cn = cn_solver(dt=dt, t_prev=t_prev, i_app=i_app_,
                       R=R, S=S, D_s=D, c_smax=c_max, solver_method="TDMA")
print(cn_solver.c_prev[-1])
i_app_: float = cycler.get_current(step_name="discharge")
SOC_cn = cn_solver(dt=dt, t_prev=t_prev, i_app=i_app_,
                       R=R, S=S, D_s=D, c_smax=c_max, solver_method="TDMA")
print(cn_solver.c_prev[-1])

# solve for SOC wrt to time
lst_cn_time, lst_cn_soc = [], []
t_start = time.time()  # start timer
SOC_cn = SOC_init
while SOC_cn > 0:
    i_app_: float = cycler.get_current(step_name="discharge")
    SOC_cn = cn_solver(dt=dt, t_prev=t_prev, i_app=i_app_,
                       R=R, S=S, D_s=D, c_smax=c_max, solver_method="TDMA")
    lst_cn_time.append(t_prev)
    lst_cn_soc.append(SOC_cn)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"CN solver solved in {t_end - t_start} s")

# ----------------------------------Eigen Solver------------------------------------------------------------------------

t_prev: float = 0.0  # previous time [s]

# solve for SOC wrt to time
lst_eigen_time, lst_eigen_soc = [], []
t_start = time.time()  # start timer
while SOC_eigen > 0:
    i_app_: float = cycler.get_current(step_name="discharge")
    SOC_eigen = eigen_solver(dt=dt, t_prev=t_prev,
                             i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_eigen_time.append(t_prev)
    lst_eigen_soc.append(SOC_eigen)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"eigen solver solved in {t_end - t_start} s")

# -------------------------------------- Poly Solver -------------------------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_poly_time, lst_poly_soc = [], []
t_start = time.time()  # start timer
SOC_poly = SOC_init
while SOC_poly > 0:
    i_app_: float = cycler.get_current(step_name="discharge")
    SOC_poly = poly_solver(dt=dt, t_prev=t_prev,
                           i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_poly_time.append(t_prev)
    lst_poly_soc.append(SOC_poly)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"Poly solver solved in {t_end - t_start} s")

# -------------------------------------- Poly Solver - Two Order -------------------------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_poly_time_two, lst_poly_soc_two = [], []
t_start = time.time()  # start timer
SOC_poly_two = SOC_init
while SOC_poly_two > 0:
    i_app_: float = cycler.get_current(step_name="discharge")
    SOC_poly_two: float = poly_solver_two(dt=dt, t_prev=t_prev,
                                          i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_poly_time_two.append(t_prev)
    lst_poly_soc_two.append(SOC_poly_two)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"Poly solver - Two Order - solved in {t_end - t_start} s")

# ----------------------------------------------Save Results-----------------------------------------------------------

FILE_DIR: str = pathlib.Path(__file__).parent.__str__()

with open(os.path.join(FILE_DIR, "saved_results", "neg_discharge_eigen_time.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_time, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "neg_discharge_eigen_soc.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_soc, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "neg_discharge_cn_time.pkl"), "wb") as pkl_cn_file:
    pickle.dump(lst_cn_time, pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "neg_discharge_cn_soc.pkl"), "wb") as pkl_cn_file:
    pickle.dump(lst_cn_soc, pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "neg_discharge_poly_time.pkl"), "wb") as pkl_poly_file:
    pickle.dump(lst_poly_time, pkl_poly_file)

with open(os.path.join(FILE_DIR, "saved_results", "neg_discharge_poly_soc.pkl"), "wb") as pkl_poly_file:
    pickle.dump(lst_poly_soc, pkl_poly_file)

with open(os.path.join(FILE_DIR, "saved_results", "neg_discharge_poly_two_time.pkl"), "wb") as pkl_poly_two_file:
    pickle.dump(lst_poly_time_two, pkl_poly_two_file)

with open(os.path.join(FILE_DIR, "saved_results", "neg_discharge_poly_two_soc.pkl"), "wb") as pkl_poly_two_file:
    pickle.dump(lst_poly_soc_two, pkl_poly_two_file)


# ----------------------------------------------Plots------------------------------------------------------------------

plt.plot(lst_cn_time, lst_cn_soc, label="Crank-Nicolson Scheme")
plt.plot(lst_eigen_time, lst_eigen_soc, label="Eigen Expansion Method")
plt.plot(lst_poly_time, lst_poly_soc, label="Polynomial Approximation")
plt.plot(lst_poly_time_two, lst_poly_soc_two,
         label="Polynomial Approximation - Two Order")

plt.xlabel("Time [s]")
plt.ylabel("Negative Electrode SOC")
plt.legend()
plt.show()
