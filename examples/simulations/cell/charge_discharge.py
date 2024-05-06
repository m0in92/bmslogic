"""
This module is an example implementation of SPCPPy using the parameter_sets for a cycling step involving charge, rest, discharge, and rest steps.
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
    charge_current: float = 1.5
    discharge_current: float = 1.5
    soc_lib_min: float = 0.0
    soc_lib_max: float = 1.0
    V_min: float = 2.5
    V_max: float = 4.2
    rest_time: float = 3600  # in seconds
    soc_p_init: float = 0.9464153612484812
    soc_n_init: float = 0.04495402282492643

    battery_cell: sp.BatteryCell = sp.ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=soc_n_init,
                                                                                               soc_p_init=soc_p_init,
                                                                                               T_amb=T,
                                                                                               R_cell=R_cell)
    cycler: sp.ChargeDischarge = sp.ChargeDischarge(charge_current=charge_current, discharge_current=discharge_current,
                                                      V_min=V_min, V_max=V_max,
                                                      soc_min=soc_lib_min, soc_max=soc_lib_max, soc=0.0,
                                                      rest_time=rest_time)

    solver: sp.BatterySolver =sp.BatterySolver(battery_cell=battery_cell, 
                                                  is_isothermal=True, 
                                                  enable_degradation=False)
    sol: sp.Solution = solver.solve(cycler=cycler)
    
    # plots
    sp.Plot(sol=sol).plot_comprehensive()
    