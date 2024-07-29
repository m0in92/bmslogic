"""
Example script for the usage of Crank Nicolson method for the electrode surface SOC calculations
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."
__status__ = "Deployed"

import time
import random

import numpy as np
import matplotlib.pyplot as plt

try:
    from bmslogic.simulations.cell.cell import PolySolver, SPKFPolynomialApprox
except ModuleNotFoundError as e:
    import sys
    import pathlib

    sys.path.append(pathlib.Path(__file__).parent.parent.parent.parent.parent.__str__())
    from bmslogic.simulations.cell.cell import PolySolver, SPKFPolynomialApprox


# Electrode parameters below
R = 1.25e-5  # electrode particle radius in [m]
c_max = 31833  # max. electrode concentration [mol/m3]
D = 3.9e-14  # electrode diffusivity [m2/s]
S = 0.7824  # electrode electrochemical active area [m2]
SOC_init = 0.7568  # initial electrode SOC

# Simulation parametes below
i_app = -1.65  # Applied current [A]
dt = 0.1  # time increment [s]
N_sim: int = 3600

poly_solver_instance: PolySolver = PolySolver(electrode_type='n', c_init=c_max*SOC_init, solver_type="higher")
spkf_solver_instance: SPKFPolynomialApprox = SPKFPolynomialApprox('n', c_max*SOC_init, R, S, D, 100, 100, 100)

# Poly simulation iteration below
t_prev = 0  # previous time [s]
lst_poly_time, lst_poly_soc = [], []
t_start = time.time()  # start timer
SOC_ = SOC_init
while SOC_ > 0:
    poly_solver_instance.solve(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D=D)
    SOC_ = poly_solver_instance.c_s

    lst_poly_time.append(t_prev)
    lst_poly_soc.append(SOC_)

    t_prev += dt
t_end = time.time()  # end timer
print(f"Poly solver solved in {t_end - t_start} s")

# Add noise to the results of the poly solver
array_poly_soc:  np.ndarray = np.array(lst_poly_soc)
array_poly_soc_noise = array_poly_soc + np.random.normal(0, 500, len(array_poly_soc))

# SPKF simulation
t_prev = 0  # previous time [s]
lst_spkf_time, lst_spkf_soc = [], []
t_start = time.time()  # start timer
SOC_ = SOC_init
idx: int = 0
while SOC_ > 0:
    SOC_ = spkf_solver_instance.solve_spkf(dt, t_prev, i_app, lst_poly_soc[idx] * c_max) / c_max

    lst_spkf_time.append(t_prev)
    lst_spkf_soc.append(SOC_)

    t_prev += dt
    idx += 1
t_end = time.time()  # end timer
print(f"SPKF solver solved in {t_end - t_start} s")

# plots
# plt.plot(lst_poly_time, array_poly_soc_noise, label="noisy")
# plt.plot(lst_poly_time, lst_poly_soc, label="true")
plt.plot(lst_spkf_time, lst_spkf_soc)


plt.legend()
plt.show()