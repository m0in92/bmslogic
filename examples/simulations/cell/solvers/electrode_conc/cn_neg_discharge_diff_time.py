"""
Example script for the usage of Crank Nicolson method for the electrode surface SOC calculations
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
R = 1.25e-5  # electrode particle radius in [m]
c_max = 31833  # max. electrode concentration [mol/m3]
D = 3.9e-14  # electrode diffusivity [m2/s]
S = 0.7824  # electrode electrochemical active area [m2]
SOC_init = 0.7568  # initial electrode SOC

# Simulation parametes below
i_app = -1.65  # Applied current [A]
dt_1 = 0.1  # time increment [s]
dt_2 = 5  # time increment [s]
N_sim: int = 3600

solver_instance_1: CNSolver = CNSolver(c_init=c_max*SOC_init, electrode_type='n', num_spatial_pts=100)
solver_instance_2: CNSolver = CNSolver(c_init=c_max*SOC_init, electrode_type='n', num_spatial_pts=100)

# CN simulation iteration below
t_prev = 0  # previous time [s]
lst_cn_time_1, lst_cn_soc_1 = [], []
t_start = time.time()  # start timer
SOC_ = SOC_init
while SOC_ > 0:
    solver_instance_1.solve(dt=dt_1, I_app=i_app, R=R, S=S, D=D)
    SOC_ = solver_instance_1.c_s

    lst_cn_time_1.append(t_prev)
    lst_cn_soc_1.append(SOC_)

    t_prev += dt_1
t_end = time.time()  # end timer
print(f"CN solver solved in {t_end - t_start} s")

# CN simulation iteration below
t_prev = 0  # previous time [s]
lst_cn_time_2, lst_cn_soc_2 = [], []
t_start = time.time()  # start timer
SOC_ = SOC_init
while SOC_ > 0:
    solver_instance_2.solve(dt=dt_2, I_app=i_app, R=R, S=S, D=D)
    SOC_ = solver_instance_2.c_s

    lst_cn_time_2.append(t_prev)
    lst_cn_soc_2.append(SOC_)

    t_prev += dt_2
t_end = time.time()  # end timer
print(f"CN solver solved in {t_end - t_start} s")



# plots
plt.plot(lst_cn_time_1, lst_cn_soc_1, label=f"CN-dt={dt_1}s")
plt.plot(lst_cn_time_2, lst_cn_soc_2, label=f"CN-dt={dt_2}s")

plt.legend()
plt.show()
