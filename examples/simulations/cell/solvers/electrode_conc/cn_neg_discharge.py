"""
Example script for the usage of Crank Nicolson method for the electrode surface SOC calculations
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."
__status__ = "Deployed"

import time
import matplotlib.pyplot as plt

try:
    from bmslogic.simulations.cell.cell import CNSolver, PolySolver
except ModuleNotFoundError as e:
    import sys
    import pathlib

    sys.path.append(pathlib.Path(__file__).parent.parent.parent.parent.parent.parent.__str__())
    from bmslogic.simulations.cell.cell import CNSolver, PolySolver, EigenSolver


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

solver_instance: CNSolver = CNSolver(SOC_init * c_max, electrode_type='n', num_spatial_pts=100)
eigen_solver_instance: EigenSolver = EigenSolver(electrode_type='n', soc_init=SOC_init, num_roots=10)
poly_solver_instance: PolySolver = PolySolver(electrode_type='n', c_init=c_max*SOC_init, solver_type="higher")

# CN simulation iteration below
t_prev = 0  # previous time [s]
lst_cn_time, lst_cn_soc = [], []
t_start = time.time()  # start timer
SOC_ = SOC_init
while SOC_ > 0:
    solver_instance.solve(dt=dt, I_app=i_app, R=R, S=S, D=D)
    SOC_ = solver_instance.c_s

    lst_cn_time.append(t_prev)
    lst_cn_soc.append(SOC_)

    t_prev += dt
t_end = time.time()  # end timer
print(f"CN solver solved in {t_end - t_start} s")

# Eigen simulation iteration below
t_prev = 0.0  # previous time [s]
lst_eigen_time, lst_eigen_soc = [], []
t_start = time.time()  # start timer
SOC_ = SOC_init
while SOC_ > 0:
    SOC_ = eigen_solver_instance.solve(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D=D, c_s_max=c_max) * c_max

    lst_eigen_time.append(t_prev)
    lst_eigen_soc.append(SOC_)

    t_prev += dt
t_end = time.time()  # end timer
print(f"Eigen solver solved in {t_end - t_start} s")

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

# plots
plt.plot(lst_cn_time, lst_cn_soc, label="CN")
# plt.plot(lst_eigen_time, lst_eigen_soc, label="eigen")
# plt.plot(lst_poly_time, lst_poly_soc, label="poly")

plt.legend()
plt.show()