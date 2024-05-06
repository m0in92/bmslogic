"""
This module is an example implementation of SPCPPy using the NElectrode, PElectrode, Electrolyte, and BatteryCell class.
"""

__author__ = "Moin Ahmed"
__copyright__ = 'Copyright 2024 by SPCPPy. All rights reserved.'
__status__ = 'deployed'

import time

import numpy as np
# import matplotlib.pyplot as plt

import build.bmslogic.simulations.cell.Debug.cell as sp
from bmslogic.simulations.cell.plot import Plot

from examples.simulations.cell.example_parameter import *


if __name__ == "__main__":
    SOC_init_p: float = 0.4952
    SOC_init_n: float = 0.7522

    p_electrode: sp.PElectrode = sp.PElectrode(L=L_p, A=A_p, kappa=kappa_p, epsilon=epsilon_p, max_conc=max_conc_p, R=R_p, S=S_p,
                                               T_ref=T_ref_p, D_ref=D_ref_p, k_ref=k_ref_p, Ea_D=Ea_D_p, Ea_R=Ea_R_p, alpha=alpha_p,
                                               brugg=brugg_p, SOC=SOC_init_p, T=T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
    n_electrode: sp.NElectrode = sp.NElectrode(L=L_n, A=A_n, kappa=kappa_n, epsilon=epsilon_n, max_conc=max_conc_n, R=R_n, S=S_n, 
                                               T_ref=T_ref_n, D_ref=D_ref_n, k_ref=k_ref_n, Ea_D=Ea_D_n, Ea_R=Ea_R_n, alpha=alpha_n,
                                               brugg=brugg_n, SOC=SOC_init_n, T=T, func_OCP=OCP_ref_n, func_dOCPdT=dOCPdT_n)
    electrolyte: sp.Electrolyte = sp.Electrolyte(L=L_e, conc=c_init_e, kappa=kappa_e, epsilon=epsilon_e, brugg=brugg_e)
    battery_cell: sp.BatteryCell = sp.BatteryCell(p_elec=p_electrode, n_elec=n_electrode, electrolyte=electrolyte,
                                                  rho=rho, Vol=Vol, C_p=C_p, h=h, A=A, cap=cap, V_max=V_max, V_min=V_min, R_cell=R_cell)
    dc: sp.Discharge = sp.Discharge(current=discharge_current, V_min=V_min, soc_lib_min=soc_lib_min, soc_lib=soc_lib)

    solver: sp.BatterySolver =sp.BatterySolver(battery_cell=battery_cell, 
                                                  is_isothermal=False, 
                                                  enable_degradation=False)
    sol: sp.Solution = solver.solve(cycler=dc)
    
    # plots
    Plot(sol=sol).plot_comprehensive()


