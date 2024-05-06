"""
This module is an example implementation of SPCPPy using the NElectrode, PElectrode, Electrolyte, and BatteryCell class using the custom cycler.
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
    soc_lib_min: float = 0.0
    soc_lib_max: float = 1.0
    V_min: float = 2.5
    V_max: float = 4.2
    soc_lib: float = 0.0

    battery_cell: sp.BatteryCell = sp.ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
                                                                                               soc_p_init=SOC_init_p,
                                                                                               T_amb=T,
                                                                                               R_cell=R_cell)
    
    t: np.ndarray = np.linspace(0, 5000, 100 * 3601)
    I: np.ndarray = -1.656 * np.ones(len(t))
    cycler: sp.CustomCycler = sp.CustomCycler(t_array=t, current_array=I,
                                              V_min=V_min, V_max=V_max,
                                              soc_lib_min=soc_lib_min, soc_lib_max=soc_lib_max,
                                              soc_lib=soc_lib)
    solver: sp.BatterySolver =sp.BatterySolver(battery_cell=battery_cell, 
                                                  is_isothermal=True, 
                                                  enable_degradation=False)
    sol: sp.Solution = solver.solve(cycler=cycler)
    
    # plots
    sp.Plot(sol=sol).plot_comprehensive()

    

