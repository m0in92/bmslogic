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

from bmslogic import cell_sim


electrode_temp = 298.15

SOC_LCO: np.ndarray = np.linspace(0.39, 1)
OCP_LCO: np.ndarray = cell_sim.general_ocps.LCO(soc = SOC_LCO)

SOC_NMC: np.ndarray = np.linspace(0.39, 0.99)
OCP_NMC: np.ndarray = cell_sim.general_ocps.NMC(soc=SOC_NMC)

SOC_LMO: np.ndarray = np.linspace(0.18, 0.95)
OCP_LMO: np.ndarray = cell_sim.general_ocps.LMO(soc=SOC_LMO)

SOC_NCA: np.ndarray = np.linspace(0.19, 1)
OCP_NCA: np.ndarray = cell_sim.general_ocps.NCA(soc=SOC_NCA)

SOC_LFP: np.ndarray = np.linspace(0.05, 1)
OCP_LFP: np.ndarray = cell_sim.general_ocps.LFP(soc=SOC_LFP)

print("LCO OCP when SOC = 0.4: ", cell_sim.general_ocps.LCO(soc=0.4))
print("NMC OCP when SOC = 0.4: ", cell_sim.general_ocps.NMC(soc=0.4))
print("LMO OCP when SOC = 0.4: ", cell_sim.general_ocps.LMO(soc=0.4))
print("NCA OCP when SOC = 0.4: ", cell_sim.general_ocps.NCA(soc=0.4))
print("LFP OCP when SOC = 0.4: ", cell_sim.general_ocps.LFP(soc=0.4))

plt.hlines(4.3, 0, 1, colors='red', linestyles='--')
plt.plot(SOC_LCO, OCP_LCO, label="LCO")
plt.plot(SOC_NMC, OCP_NMC, label="NMC")
plt.plot(SOC_LMO, OCP_LMO, label="LMO")
plt.plot(SOC_NCA, OCP_NCA, label="NCA")
plt.plot(SOC_LFP, OCP_LFP, label="LFP")

plt.xlabel("SOC")
plt.ylabel("OCP [V]")

plt.title("OCP of Positive Electrodes at 298.15 K")

plt.legend()
plt.show()



