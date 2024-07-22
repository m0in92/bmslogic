"""
This module is an example implementation of SPCPPy using the parameter_sets under hppc discharge steps.
"""

__author__ = "Moin Ahmed"
__copyright__ = 'Copyright 2024 by SPCPPy. All rights reserved.'
__status__ = 'deployed'

import time
import os
import pathlib
import pickle
import sys

import numpy as np
import matplotlib.pyplot as plt

try:
    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell import pycyclers
    from bmslogic.simulations.cell.plot import Plot

    from examples.simulations.cell.example_parameter import *

except ModuleNotFoundError as e:
    PROJECT_DIR: str = pathlib.Path(
        __file__).parent.parent.parent.parent.__str__()
    print(PROJECT_DIR)
    sys.path.append(PROJECT_DIR)

    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    from bmslogic.simulations.cell import pycyclers
    from bmslogic.simulations.cell.plot import Plot

    from examples.simulations.cell.example_parameter import *


if __name__ == "__main__":
    SOC_init_p: float = 0.4952
    SOC_init_n: float = 0.7522
    i_app: float = 1.5
    kappa_e = 1e-3
    brugg_e: float = 1.5

    p_electrode: cell_sim.PElectrode = cell_sim.PElectrode(L=L_p, A=A_p, kappa=kappa_p, epsilon=epsilon_p, max_conc=max_conc_p, R=R_p, S=S_p,
                                                           T_ref=T_ref_p, D_ref=D_ref_p, k_ref=k_ref_p, Ea_D=Ea_D_p, Ea_R=Ea_R_p, alpha=alpha_p,
                                                           brugg=brugg_p, SOC=SOC_init_p, T=T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
    n_electrode: cell_sim.NElectrode = cell_sim.NElectrode(L=L_n, A=A_n, kappa=kappa_n, epsilon=epsilon_n, max_conc=max_conc_n, R=R_n, S=S_n,
                                                           T_ref=T_ref_n, D_ref=D_ref_n, k_ref=k_ref_n, Ea_D=Ea_D_n, Ea_R=Ea_R_n, alpha=alpha_n,
                                                           brugg=brugg_n, SOC=SOC_init_n, T=T, func_OCP=OCP_ref_n, func_dOCPdT=dOCPdT_n)
    cycler: pycyclers.HPPCCycler = pycyclers.HPPCCycler(t1=500, t2=100, i_app=i_app,
                                                        charge_or_discharge='discharge',
                                                        V_min=2.5, V_max=4.2, soc_lib_min=0.0,
                                                        soc_lib_max=1.0, soc_lib=1.0, hppc_steps=100)
    electrolyte: cell_sim.Electrolyte = cell_sim.Electrolyte(
        L=L_e, conc=c_init_e, kappa=kappa_e, epsilon_n=epsilon_en, epsilon=epsilon_e, epsilon_p=epsilon_ep, D_e=D_e, t_c=t_c, brugg=brugg_e)
    battery_cell: cell_sim.BatteryCell = cell_sim.BatteryCell(p_elec=p_electrode, n_elec=n_electrode, electrolyte=electrolyte,
                                                              rho=rho, Vol=Vol, C_p=C_p, h=h, A=A, cap=cap, V_max=V_max, V_min=V_min, R_cell=R_cell)

    solver_spm: cell_sim.BatterySolver = cell_sim.BatterySolver(battery_cell=battery_cell,
                                                                       is_isothermal=True,
                                                                       enable_degradation=False)
    sol_spm: cell_sim.Solution = solver_spm.solve(cycler=cycler)

    # plots
    # plt.plot(sol_spm.t, sol_spm.V)
    plt.plot(sol_spm.t, sol_spm.overpotential_elec_p)
    plt.plot(sol_spm.t, sol_spm.overpotential_elec_n)
    plt.plot(sol_spm.t, sol_spm.overpotential_R_cell)
    plt.plot(sol_spm.t, sol_spm.overpotential_electrolyte)

    plt.show()
