"""
Example of using the package's open-circuit potential. 

These open-circuit potential can be used in case the user does not know the specific open-circuit potential relation with soc.
"""

__all__ = []

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."
__status__ = "Deployed"


import numpy as np
import matplotlib.pyplot as plt

try:
    from bmslogic import cell_sim
except ModuleNotFoundError as e:
    import sys
    import pathlib

    sys.path.append(pathlib.Path(__file__).parent.parent.parent.parent.parent.__str__())
    from bmslogic.parameter_sets.test.funcs import OCP_ref_n, OCP_ref_p
    from bmslogic import cell_sim


SOC_graphite: np.ndarray = np.linspace(0, 0.8)
OCP_graphite: np.ndarray = cell_sim.general_ocps.graphite(soc=SOC_graphite)

print("LCO OCP when SOC = 0.4: ", cell_sim.general_ocps.graphite(soc=0.4))


plt.plot(SOC_graphite, OCP_graphite)

plt.xlabel("SOC")
plt.ylabel("OCP [V]")

plt.title("OCP of Negative Electrodes at 298.15 K")
plt.show()
