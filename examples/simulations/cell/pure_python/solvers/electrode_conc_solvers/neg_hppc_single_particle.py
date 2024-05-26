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
from bmslogic.simulations.cell.cyclers import PyDischargeRest, PyHPPCCycler
from bmslogic.simulations.cell.solvers.electrode_conc import PyEigenFuncExp, PyCNSolver, PyPolynomialApproximation


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
rest_time: float = 3600  # [s]

# initiate solver instances below
eigen_solver: PyEigenFuncExp = PyEigenFuncExp(
    x_init=SOC_init, n=5, electrode_type='n')
cn_solver: PyCNSolver = PyCNSolver(c_init=SOC_init*c_max, electrode_type='n')
poly_solver: PyPolynomialApproximation = PyPolynomialApproximation(
    c_init=SOC_init*c_max, electrode_type='n', type='higher')
poly_solver_two: PyPolynomialApproximation = PyPolynomialApproximation(
    c_init=SOC_init*c_max, electrode_type='n', type='two')

# initiate cycler instance. Note that the cyclers are programmed to be used for the battery cells and not for specific solvers.
# Hence there has to be some compromise in their usage in this script.
cycler: PyHPPCCycler = PyHPPCCycler(
    t1=50, t2=100, i_app=i_app, charge_or_discharge='discharge', V_min=2.5, V_max=4.2, soc_lib_min=0.0,
                                                        soc_lib_max=1.0, soc_lib=1.0, hppc_steps=100)

# # -------------------------------------- CN Solver ---------------------------------------------------------------------

# # Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_cn_time, lst_cn_soc = [], []
t_start = time.time()  # start timer
soc_ = SOC_init
while soc_ > 0.0189023:
    i_app_: float = cycler.get_current(step_name="discharge", t=t_prev)
    soc_ = cn_solver(dt=dt, t_prev=t_prev, i_app=i_app_,
                     R=R, S=S, D_s=D, c_smax=c_max, solver_method="TDMA")
    lst_cn_time.append(t_prev)
    lst_cn_soc.append(soc_)

    t_prev += dt  # update the time

t_end = time.time()  # end timer
cycler.reset()
print(f"CN solver solved in {t_end - t_start} s")

# ----------------------------------EIGEN SOLVER------------------------------------------------------------------------

t_prev: float = 0.0  # previous time [s]

# solve for SOC wrt to time
lst_eigen_time, lst_eigen_soc = [], []
t_start = time.time()  # start timer
soc_ = SOC_init
while SOC_eigen > 0.0189023:
    i_app_: float = cycler.get_current(step_name="discharge", t=t_prev)
    SOC_eigen = eigen_solver(dt=dt, t_prev=t_prev,
                             i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_eigen_time.append(t_prev)
    lst_eigen_soc.append(SOC_eigen)

    t_prev += dt  # update the time

t_end = time.time()  # end timer
cycler.reset()
print(f"eigen solver solved in {t_end - t_start} s")

# -------------------------------------- POLYSOLVER  - HIGHER ORDER -------------------------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_poly_time, lst_poly_soc = [], []
t_start = time.time()  # start timer
SOC_poly = SOC_init
while SOC_poly > 0.0189023:
    i_app_: float = cycler.get_current(step_name="discharge", t=t_prev)
    SOC_poly = poly_solver(dt=dt, t_prev=t_prev,
                           i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_poly_time.append(t_prev)
    lst_poly_soc.append(SOC_poly)

    t_prev += dt  # update the time

t_end = time.time()  # end timer
cycler.reset()
print(f"Poly solver solved in {t_end - t_start} s")

# ----------------------------------------------Save Results-----------------------------------------------------------

FILE_DIR: str = pathlib.Path(__file__).parent.__str__()

with open(os.path.join(FILE_DIR, "saved_results" , "neg_hppc_cn_time.pkl"), "wb") as pkl_cn_file:
    pickle.dump(lst_cn_time, pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results" , "neg_hppc_cn_soc.pkl"), "wb") as pkl_cn_file:
    pickle.dump(lst_cn_soc, pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results" , "neg_hppc_eigen_time.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_time, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results" , "neg_hppc_eigen_soc.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_soc, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results" , "neg_hppc_poly_time.pkl"), "wb") as pkl_poly_file:
    pickle.dump(lst_poly_time, pkl_poly_file)

with open(os.path.join(FILE_DIR, "saved_results" , "neg_hppc_poly_soc.pkl"), "wb") as pkl_poly_file:
    pickle.dump(lst_poly_soc, pkl_poly_file)

# --------------------------------PLOTS-----------------------------------------------------------
plt.plot(lst_cn_time, lst_cn_soc, label="CN")
plt.plot(lst_eigen_time, lst_eigen_soc, label="eigen")
plt.plot(lst_poly_time, lst_poly_soc, label="poly-higher")

plt.legend()
plt.show()
