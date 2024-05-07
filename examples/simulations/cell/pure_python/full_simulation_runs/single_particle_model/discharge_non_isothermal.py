"""
This script contains the example usage of the single particle model for the discharge operation under non-isothermal conditions.
"""

__all__ = []

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2024 by BMSLogic. All rights reserved.'
__status__ = 'Deployed'


from bmslogic import cell_sim


# Operating parameters
I: float = 1.656
temp: float = 298.15
V_min: float = 3
SOC_min: float = 0.1
soc_lib_init: float = 1.0

# Modelling parameters
SOC_init_p: float = 0.4956  # from Guo et. al.
SOC_init_n: float = 0.7568  # from Guo et. al.

# Setup battery components
cell: cell_sim.PyBatteryCell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                                              soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                              temp_init=temp)

# set-up cycler and solver
dc: cell_sim.PyDischarge = cell_sim.PyDischarge(discharge_current=I, v_min=V_min,
                                                SOC_LIB_min=SOC_min, SOC_LIB=soc_lib_init)
solver: cell_sim.PySPSolver = cell_sim.PySPSolver(b_cell=cell,
                                                  isothermal=False, degradation=False,
                                                  electrode_SOC_solver='poly')

# simulate
sol = solver.solve(cycler_instance=dc)

# Plot
sol.comprehensive_plot()
