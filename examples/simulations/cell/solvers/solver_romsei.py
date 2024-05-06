import numpy as np
import matplotlib.pyplot as plt

from cpp_modules.solvers import ROMSEISolver
import SPCPPY as sp

from examples.example_parameter import OCP_ref_n


k: float = 1.76e-11
c_e: float = 1000.0
S: float = 0.7824
c_s_max: float = 31833
U_s: float = 0.4
j_0_s: float = 1.14264e-15
A: float = 0.0596
MW: float = 0.16
rho: float = 1600
kappa: float = 5e-6
temp: float = 298.15

solver: ROMSEISolver = ROMSEISolver(k=1.76e-11, c_e=1000.0, S=0.7824, c_s_max=31833,
                                    U_s=0.4, j_0_s=1.14264e-15, A=0.0596, MW=0.16,
                                    rho=1600, kappa=5e-6)

# I_i: list = []
I_s: list = []
soc_n: np.ndarray = np.linspace(0.01, 0.7568)
for i, soc_ in enumerate(soc_n):
    ocp_: float = OCP_ref_n(SOC=soc_)
    I_s_ = solver.calc_current(soc=soc_, ocp=ocp_, temp=temp, i_app=1.656, relative_tolerance=1e-15)
    I_s.append(I_s_)

# print(I_i)

# plots
fig, ax1 = plt.subplots()
ax1.plot(soc_n, I_s, label="I_s")

plt.legend()
plt.show()
