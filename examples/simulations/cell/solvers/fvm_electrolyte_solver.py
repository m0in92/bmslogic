import time

import numpy as np
import matplotlib.pyplot as plt

from bmslogic.simulations.cell.cell import ElectrolyteFVMCoordinates, ElectrolyteFVMSolver


L_n: float = 8e-5
L_sep: float = 2.5e-5
L_p: float = 8.8e-5

epsilon_e_n: float = 0.385
epsilon_e_sep: float = 0.785
epsilon_e_p: float = 0.485

D_e: float = 3.5e-10  # [m2/s]
brugg: float = 4
t_c: float = 0.354
c_e_init = 1000  # [mol/m3]

a_s_n: float = 5.78e3
a_s_p: float = 7.28e3


# Simulation parameters
dt: float = 0.1  # [s]
max_iter: int = 1000

coords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(
    L_n=L_n, L_sep=L_sep, L_p=L_p)
solver: ElectrolyteFVMSolver = ElectrolyteFVMSolver(fvm_coords=coords, c_e_init=c_e_init, t_c=t_c,
                                                    epsilon_e_n=epsilon_e_n, epsilon_e_sep=epsilon_e_sep, epsilon_e_p=epsilon_e_p,
                                                    a_s_n=a_s_n, a_s_p=a_s_p,
                                                    D_e=D_e, brugg=brugg)

j_p = -1.53693327e-05 * np.ones(10)  # [mol/m2/s]
j_sep = np.zeros(10)  # [mol/m2/s]
j_n = 2.19362652e-05 * np.ones(10)  # [mol/m2/s]
j = np.append(np.append(j_n, j_sep), j_p)  # [mol/m2/s]

time_start = time.time()
for i in range(max_iter):
    solver.solve(j=j, dt=dt)
time_end = time.time()

print("Simulation loop time: ", time_end - time_start, " s")

plt.plot(solver.array_c_e)
plt.show()
