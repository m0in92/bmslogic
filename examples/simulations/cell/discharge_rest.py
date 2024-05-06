"""
This module is an example implementation of SPCPPy using the parameter_sets for a cycling step involving discharge and rest steps.
"""

__author__ = "Moin Ahmed"
__copyright__ = 'Copyright 2024 by SPCPPy. All rights reserved.'
__status__ = 'deployed'

import time

import numpy as np
import matplotlib.pyplot as plt

import SPCPPY as sp

from examples.example_parameter import *


if __name__ == "__main__":
    SOC_init_p: float = 0.4952
    SOC_init_n: float = 0.7522
    
    battery_cell: sp.BatteryCell = sp.ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
                                                                                               soc_p_init=SOC_init_p,
                                                                                               T_amb=T,
                                                                                               R_cell=R_cell)
    dc: sp.Discharge = sp.DischargeRest(current=discharge_current, V_min=V_min, soc_lib_min=soc_lib_min, soc_lib=soc_lib,
                                        rest_time = 3600)

    solver: sp.BatterySolver =sp.BatterySolver(battery_cell=battery_cell, 
                                                  is_isothermal=True, 
                                                  enable_degradation=False)
    sol: sp.Solution = solver.solve(cycler=dc)

    # examples of simulation results
    print("soc_p the end of the simulation: ", sol.soc_p[-1],
          "soc_n the end of the simulation: ", sol.soc_n[-1])
    
    # plots
    sp.Plot(sol=sol).plot_comprehensive()


