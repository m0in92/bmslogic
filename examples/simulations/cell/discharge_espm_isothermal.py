"""
This module is an example implementation of cell_simCPPy using the NElectrode, PElectrode, Electrolyte, and BatteryCell class.
"""

__author__ = "Moin Ahmed"
__copyright__ = 'Copyright 2024 by cell_simCPPy. All rights reserved.'
__status__ = 'deployed'

import time
import os
import pathlib
import pickle
import sys

import numpy as np

try:
    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell.plot import Plot

    from examples.simulations.cell.example_parameter import *

except ModuleNotFoundError as e:
    PROJECT_DIR: str = pathlib.Path(
        __file__).parent.parent.parent.parent.__str__()
    print(PROJECT_DIR)
    sys.path.append(PROJECT_DIR)

    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell.plot import Plot

    from examples.simulations.cell.example_parameter import *


if __name__ == "__main__":
    SOC_init_p: float = 0.4952
    SOC_init_n: float = 0.7522

    p_electrode: cell_sim.PElectrode = cell_sim.PElectrode(L=L_p, A=A_p, kappa=kappa_p, epsilon=epsilon_p, max_conc=max_conc_p, R=R_p, S=S_p,
                                                           T_ref=T_ref_p, D_ref=D_ref_p, k_ref=k_ref_p, Ea_D=Ea_D_p, Ea_R=Ea_R_p, alpha=alpha_p,
                                                           brugg=brugg_p, SOC=SOC_init_p, T=T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
    n_electrode: cell_sim.NElectrode = cell_sim.NElectrode(L=L_n, A=A_n, kappa=kappa_n, epsilon=epsilon_n, max_conc=max_conc_n, R=R_n, S=S_n,
                                                           T_ref=T_ref_n, D_ref=D_ref_n, k_ref=k_ref_n, Ea_D=Ea_D_n, Ea_R=Ea_R_n, alpha=alpha_n,
                                                           brugg=brugg_n, SOC=SOC_init_n, T=T, func_OCP=OCP_ref_n, func_dOCPdT=dOCPdT_n)
    electrolyte: cell_sim.Electrolyte = cell_sim.Electrolyte(
        L=L_e, conc=c_init_e, kappa=kappa_e, epsilon_n=epsilon_en, epsilon=epsilon_e, epsilon_p=epsilon_ep, D_e=D_e, t_c=t_c, brugg=brugg_e)
    battery_cell: cell_sim.BatteryCell = cell_sim.BatteryCell(p_elec=p_electrode, n_elec=n_electrode, electrolyte=electrolyte,
                                                              rho=rho, Vol=Vol, C_p=C_p, h=h, A=A, cap=cap, V_max=V_max, V_min=V_min, R_cell=R_cell)
    dc: cell_sim.Discharge = cell_sim.Discharge(
        current=discharge_current, V_min=V_min, soc_lib_min=soc_lib_min, soc_lib=soc_lib)

    solver: cell_sim.ESPBatterySolver = cell_sim.ESPBatterySolver(battery_cell=battery_cell,
                                                            is_isothermal=True,
                                                            enable_degradation=False)
    sol: cell_sim.Solution = solver.solve(cycler=dc)

    # plots
    Plot(sol=sol).plot_comprehensive()
