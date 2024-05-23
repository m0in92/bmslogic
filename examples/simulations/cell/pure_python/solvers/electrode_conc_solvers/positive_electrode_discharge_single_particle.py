import pathlib 
import pickle
import os

import time
import matplotlib.pyplot as plt

from bmslogic.simulations.cell.cyclers import PyCharge
from bmslogic.simulations.cell.solvers.electrode_conc import PyEigenFuncExp, PyCNSolver, PyPolynomialApproximation


# Electrode parameters below
R = 8.5e-6  # electrode particle radius in [m]
c_max = 51410  # max. electrode concentration [mol/m3]
D = 1e-14  # electrode diffusivity [m2/s]
S = 1.1167  # electrode electrochemical active area [m2]
SOC_init = 0.4956  # initial electrode SOC

# initiate solver instances below
eigen_solver = PyEigenFuncExp(x_init=SOC_init, n=5, electrode_type='p')
cn_solver = PyCNSolver(c_init=c_max*SOC_init, electrode_type='p')
poly_solver = PyPolynomialApproximation(
    c_init=SOC_init*c_max, electrode_type='p', type='higher')

# Simulation parameters below
i_app = -1.65  # Applied current [A]
SOC_eigen = SOC_init  # electrode current SOC
dt = 0.1  # time increment [s]

# initiate the cycler instance below.
cycler: PyCharge = PyCharge(charge_current=i_app, V_max=4.2, SOC_LIB_max=1.0, SOC_LIB=0.0)

# -------------------------------------- CN Solver ---------------------------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_cn_time, lst_cn_soc = [], []
t_start = time.time()  # start timer
SOC_cn = SOC_init
while SOC_cn < 1:
    i_app_: float = cycler.get_current(step_name="charge")
    SOC_cn = cn_solver(dt=dt, t_prev=t_prev, i_app=i_app_,
                       R=R, S=S, D_s=D, c_smax=c_max)
    lst_cn_time.append(t_prev)
    lst_cn_soc.append(SOC_cn)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"CN solver solved in {t_end - t_start} s")

# ----------------------------------Eigen Solver------------------------------------------------------------------------

t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_eigen_time, lst_eigen_soc = [], []
t_start = time.time()  # start timer
while SOC_eigen < 1:
    i_app_: float = cycler.get_current(step_name="charge")
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
while SOC_poly < 1:
    i_app_: float = cycler.get_current(step_name="charge")
    SOC_poly = poly_solver(dt=dt, t_prev=t_prev,
                           i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_poly_time.append(t_prev)
    lst_poly_soc.append(SOC_poly)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"Poly solver solved in {t_end - t_start} s")

# ----------------------------------------------Save Results-----------------------------------------------------------

FILE_DIR: str = pathlib.Path(__file__).parent.__str__()

with open(os.path.join(FILE_DIR, "positive_electrode_discharge_eigen_time.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_time, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "positive_electrode_discharge_eigen_soc.pkl"), "wb") as pkl_eigen_file:
    pickle.dump(lst_eigen_soc, pkl_eigen_file)

with open(os.path.join(FILE_DIR, "positive_electrode_discharge_cn_time.pkl"), "wb") as pkl_cn_file:
    pickle.dump(lst_cn_time, pkl_cn_file)

with open(os.path.join(FILE_DIR, "positive_electrode_discharge_cn_soc.pkl"), "wb") as pkl_cn_file:
    pickle.dump(lst_cn_soc, pkl_cn_file)

with open(os.path.join(FILE_DIR, "positive_electrode_discharge_poly_time.pkl"), "wb") as pkl_poly_file:
    pickle.dump(lst_poly_time, pkl_poly_file)

with open(os.path.join(FILE_DIR, "positive_electrode_discharge_poly_soc.pkl"), "wb") as pkl_poly_file:
    pickle.dump(lst_poly_soc, pkl_poly_file)

# ----------------------------------------------Plots------------------------------------------------------------------

plt.plot(lst_cn_time, lst_cn_soc, label="Crank-Nicolson Scheme")
plt.plot(lst_eigen_time, lst_eigen_soc, label="Eigen Expansion Method")
plt.plot(lst_poly_time, lst_poly_soc, label="Polynomial Approximation")

plt.xlabel("Time [s]")
plt.ylabel("Positive Electrode SOC")
plt.legend()
plt.show()
