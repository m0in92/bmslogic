"""
Contains an example of using electrolyte potential solver in a simulation. The solver uses numerical finite volume
method (FVM).
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright SPPy 2024. All rights reserved."
__status__ = "Development"


import numpy as np
import matplotlib.pyplot as plt

try:
    from bmslogic.simulations.cell.solvers.coords import PyElectrolyteFVMCoordinates
    from bmslogic.simulations.cell.solvers.electrolyte_conc import PyElectrolyteConcFVMSolver
    from bmslogic.simulations.cell.solvers.electrolyte_potential import PyElectrolytePotentialFVMSolver
    from bmslogic.simulations.cell.models import PySPMe
except ModuleNotFoundError:
    import sys
    import pathlib
    PROJECT_DIR: str = pathlib.Path(
        __file__).parent.parent.parent.parent.parent.parent.parent.__str__()
    print(PROJECT_DIR)
    sys.path.append(PROJECT_DIR)
    from bmslogic.simulations.cell.solvers.coords import PyElectrolyteFVMCoordinates
    from bmslogic.simulations.cell.solvers.electrolyte_conc import PyElectrolyteConcFVMSolver
    from bmslogic.simulations.cell.solvers.electrolyte_potential import PyElectrolytePotentialFVMSolver, PyElectrolytePotentialVolAvgSolver
    from bmslogic.simulations.cell.models import PySPMe


# Battery cell parameters
L_n: float = 8e-5
L_s: float = 2.5e-5
L_p: float = 8.8e-5

epsilon_ep: float = 0.485
epsilon_sep: float = 0.785
epsilon_en: float = 0.385
a_s_p: float = 7.28e3
a_s_n: float = 5.78e3
brugg: float = 4
t_c: float = 0.354
kappa_e: float = 0.2875
temp: float = 298.15

kappa_en: float = kappa_e * (epsilon_en ** brugg)
kappa_es: float = kappa_e * (epsilon_sep ** brugg)
kappa_ep: float = kappa_e * (epsilon_ep ** brugg)

# Simulation parameters
dt: float = 0.1
t_end: int = 360  # [s]

co_ords: PyElectrolyteFVMCoordinates = PyElectrolyteFVMCoordinates(
    L_n=L_n, L_s=L_s, L_p=L_p)
conc_solver: PyElectrolyteConcFVMSolver = PyElectrolyteConcFVMSolver(fvm_co_ords=co_ords, transference=t_c,
                                                                     epsilon_en=epsilon_en, epsilon_esep=epsilon_sep,
                                                                     epsilon_ep=epsilon_ep,
                                                                     a_sn=a_s_n, a_sp=a_s_p,
                                                                     D_e=3.5e-10,
                                                                     brugg=brugg,
                                                                     c_e_init=1000)
phi_solver: PyElectrolytePotentialVolAvgSolver = PyElectrolytePotentialVolAvgSolver(L_n=L_n, L_s=L_s, L_p=L_p,
                                                                                kappa_en=kappa_en,
                                                                                kappa_es=kappa_es,
                                                                                kappa_ep=kappa_ep,
                                                                                t_c=t_c)
i_app: float = -1.656
j_p = PySPMe.molar_flux_electrode(
    I=-1.656, S=1.1167, electrode_type='p') * np.ones(len(co_ords.array_x_p))  # [mol/m2/s]
j_sep = np.zeros(len(co_ords.array_x_s))  # [mol/m2/s]
j_n = PySPMe.molar_flux_electrode(
    I=-1.656, S=0.7824, electrode_type='n') * np.ones(len(co_ords.array_x_n))  # [mol/m2/s]
j = np.append(np.append(j_n, j_sep), j_p)  # [mol/m2/s]

for i in range(t_end):
    conc_solver.solve_ce(j=j, dt=dt, solver_method='TDMA')

# post electrolyte concentration calculations
x_n: np.ndarray = np.linspace(0.0, L_n)
x_p: np.ndarray = np.linspace(L_n + L_s, L_n + L_s + L_p)
conc_profile_n: np.ndarray = conc_solver.array_c_e[:len(conc_solver.co_ords.array_x_n)]
# conc_profile_p: np.ndarray = conc_solver.conc_profile_p(L_value=x_

phi_en: np.ndarray = np.zeros(len(x_n))
for n_index in range(len(x_n)):
    phi_en[n_index] = phi_solver.phi_en(L_value=x_n[n_index],
                                        c_e_mid=conc_solver.array_c_e[int(len(conc_solver.array_c_e)/2)],
                                        c_e_n=conc_profile_n[n_index], c_e_in=conc_solver.c_e_n,
                                        i_app=i_app, temp=temp)

# phi_ep: np.ndarray = np.zeros(len(x_p))
# for p_index in range(len(x_p)):
#     phi_ep[p_index] = phi_solver.phi_ep(L_value=x_p[p_index],
#                                         c_e_mid=conc_solver.conc_seperator_mid(),
#                                         c_e_p=conc_profile_p[p_index], c_e_ip=conc_solver.c_e_p,
#                                         i_app=i_app, temp=temp)


# plots
plt.plot(conc_solver.co_ords.array_x, conc_solver.array_c_e)

plt.ticklabel_format(axis="x", scilimits=[-3, 1])
plt.show()