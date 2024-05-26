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
from bmslogic.simulations.cell.solvers.electrode_conc import PyPolynomialApproximation
from bmslogic.simulations.cell.cyclers import PyDischargeRest, PyChargeRest

# Electrode parameters below
R = 8.5e-6  # electrode particle radius in [m]
c_max = 51410  # max. electrode concentration [mol/m3]
D = 1e-14  # electrode diffusivity [m2/s]
S = 1.1167  # electrode electrochemical active area [m2]
SOC_init = 0.4956  # initial electrode SOC

# Simulation parameters below
i_app = 1.65  # Applied current [A]
dt = 0.1  # time increment [s]
rest_time: float = 3600  # [s]

# initiate solver instances below
poly_solver: PyPolynomialApproximation = PyPolynomialApproximation(
    c_init=SOC_init*c_max, electrode_type='n', type='higher')
poly_solver_two: PyPolynomialApproximation = PyPolynomialApproximation(
    c_init=SOC_init*c_max, electrode_type='n', type='two')

# initiate cycler instance. Note that the cyclers are programmed to be used for the battery cells and not for specific solvers.
# Hence there has to be some compromise in their usage in this script.
cycler: PyChargeRest = PyChargeRest(
    charge_current=i_app, rest_time=rest_time, V_max=2.0)

# -------------------------------------- POLYSOLVER  - HIGHER ORDER -------------------------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_poly_time, lst_poly_soc = [], []
t_start = time.time()  # start timer
soc_: float = SOC_init
while soc_ < 0.98901:
    i_app_: float = cycler.get_current(step_name="charge")
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

t_end = time.time()  # end timer
cycler.reset()
print(f"Poly solver solved in {t_end - t_start} s")

# -------------------------------------- POLYSOLVER  - TWO ORDER -------------------------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_poly_two_time, lst_poly_two_soc = [], []
t_start = time.time()  # start timer
soc_ = SOC_init
while soc_ < 0.98901:
    i_app_: float = cycler.get_current(step_name="charge")
    soc_: float = poly_solver_two(dt=dt, t_prev=t_prev,
                           i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_poly_two_time.append(t_prev)
    lst_poly_two_soc.append(soc_)

    t_prev += dt  # update the time

while cycler.time_elapsed < rest_time:
    i_app_: float = cycler.get_current(step_name="rest")
    soc_: float = poly_solver_two(dt=dt, t_prev=t_prev,
                           i_app=i_app_, R=R, S=S, D_s=D, c_smax=c_max)
    lst_poly_two_time.append(t_prev)
    lst_poly_two_soc.append(soc_)

    cycler.time_elapsed += dt
    t_prev += dt  # update the time

t_end = time.time()  # end timer
print(f"Poly solver solved in {t_end - t_start} s")

# --------------------------------SAVE RESULTS-----------------------------------------------------------
FILE_DIR: str = pathlib.Path(__file__).parent.__str__()

with open(os.path.join(FILE_DIR, "saved_results", "poly_higher_pos_discharge_time.pkl"), "wb") as pkl_file:
    pickle.dump(lst_poly_time, pkl_file)

with open(os.path.join(FILE_DIR, "saved_results", "poly_higher_pos_discharge_soc.pkl"), "wb") as pkl_file:
    pickle.dump(lst_poly_soc, pkl_file)

with open(os.path.join(FILE_DIR, "saved_results", "poly_two_pos_discharge_time.pkl"), "wb") as pkl_file:
    pickle.dump(lst_poly_two_time, pkl_file)

with open(os.path.join(FILE_DIR, "saved_results", "poly_two_pos_discharge_soc.pkl"), "wb") as pkl_file:
    pickle.dump(lst_poly_two_soc, pkl_file)

# --------------------------------PLOTS-----------------------------------------------------------
plt.plot(lst_poly_time, lst_poly_soc, label="poly-higher")
plt.plot(lst_poly_two_time, lst_poly_two_soc, label="poly-two")

plt.legend()
plt.show()
