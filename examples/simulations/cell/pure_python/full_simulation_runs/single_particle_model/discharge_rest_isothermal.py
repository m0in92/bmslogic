"""
Contains the example implementation of SPPy using a discharge and rest operation under
isothermal conditions.
"""

from bmslogic import cell_sim
import matplotlib.pyplot as plt
__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by SPPy. All rights reserved.'
__status__ = 'deployed'


"""
This script contains the example usage of the single particle model for the discharge operation under non-isothermal conditions.
"""

__all__ = []

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2024 by BMSLogic. All rights reserved.'
__status__ = 'Deployed'


# Operating parameters
I: float = 1.656
temp: float = 298.15
V_min: float = 3
SOC_min: float = 0.1
soc_lib_init: float = 1.0
rest_time: float = 500  # [s]
SOC_LIB_MAX: float = 1

# Modelling parameters
SOC_init_p: float = 0.4956  # from Guo et. al.
SOC_init_n: float = 0.7568  # from Guo et. al.

# Setup battery components
cell: cell_sim.PyBatteryCell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                                              soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                              temp_init=temp)


# set-up cycler and solver
dc: cell_sim.PyDischargeRest = cell_sim.PyDischargeRest(discharge_current=I, V_min=V_min,
                                                        SOC_LIB_min=SOC_min, SOC_LIB=soc_lib_init, 
                                                        rest_time=rest_time, SOC_LIB_max=SOC_LIB_MAX)
solver: cell_sim.PySPSolver = cell_sim.PySPSolver(b_cell=cell,
                                                  isothermal=False, degradation=False,
                                                  electrode_SOC_solver='poly')

# simulate
sol_poly = solver.solve(cycler_instance=dc)

# Plot
fig = plt.figure(figsize=(10, 3), dpi=300)
ax1 = fig.add_subplot(121)
ax1.plot(sol_poly.t, sol_poly.I)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Current [A]')

ax2 = fig.add_subplot(122)
ax2.plot(sol_poly.t, sol_poly.V, label="Polynomial Approximation", linewidth=2)
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Cell Terminal Voltage [V]')

plt.tight_layout()
plt.show()
