"""
Example script for the usage of Crank Nicolson method for the electrode surface SOC calculations.
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."
__status__ = "Deployed"

import time
import matplotlib.pyplot as plt

try:
    from bmslogic.simulations.cell.cell import CNSolver
except ModuleNotFoundError as e:
    import sys
    import pathlib

    sys.path.append(pathlib.Path(__file__).parent.parent.parent.parent.parent.parent.__str__())
    from bmslogic.simulations.cell.cell import CNSolver


# Electrode parameters below
R = 8.5e-6  # electrode particle radius in [m]
c_max = 51410  # max. electrode concentration [mol/m3]
D = 1e-14  # electrode diffusivity [m2/s]
S = 1.1167  # electrode electrochemical active area [m2]
SOC_init = 0.4956  # initial electrode SOC

# Simulation parametes below
i_app = -1.65  # Applied current [A]
dt = 0.1  # time increment [s]
N_sim: int = 3600

solver_instance: CNSolver = CNSolver(c_init=c_max*SOC_init, electrode_type='p', num_spatial_pts=100)

# Simulation iteration below
t_prev = 0  # previous time [s]
lst_cn_time, lst_cn_soc = [], []
t_start = time.time()  # start timer
SOC_ = SOC_init
while SOC_ < 0.98901:
    solver_instance.solve(dt=dt, I_app=i_app, R=R, S=S, D=D)
    SOC_ = solver_instance.c_prev[-1] / c_max

    lst_cn_time.append(t_prev)
    lst_cn_soc.append(SOC_)

    t_prev += dt
t_end = time.time()  # end timer
print(f"CN solver solved in {t_end - t_start} s")

# plots
plt.plot(lst_cn_time, lst_cn_soc)

plt.show()