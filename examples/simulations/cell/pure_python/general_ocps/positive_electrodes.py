import numpy as np
import matplotlib.pyplot as plt

from bmslogic import cell_sim


electrode_temp = 298.15

SOC_LCO: np.ndarray = np.linspace(0.39, 1)
OCP_LCO: np.ndarray = cell_sim.general_ocps.LCO(soc=SOC_LCO)

SOC_LFP: np.ndarray = np.linspace(0.05, 1)
OCP_LFP: np.ndarray = cell_sim.general_ocps.LFP(soc=SOC_LFP)

SOC_LMO: np.ndarray = np.linspace(0.18, 0.95)
OCP_LMO: np.ndarray = cell_sim.general_ocps.LMO(soc=SOC_LMO)

SOC_NCA: np.ndarray = np.linspace(0.19, 1)
OCP_NCA: np.ndarray = cell_sim.general_ocps.NCA(soc=SOC_NCA)

SOC_NMC: np.ndarray = np.linspace(0.39, 0.99)
OCP_NMC: np.ndarray = cell_sim.general_ocps.NMC(soc=SOC_NMC)

a_min_LCO: float = OCP_LCO[0]
a_min_LMO: float = OCP_LMO[0]
a_min_NCA: float = OCP_NCA[0]
a_min_NMC: float = OCP_NMC[0]

a_max_LCO: float = OCP_LCO[-1]
a_max_LMO: float = OCP_LMO[-1]
a_max_NCA: float = OCP_NCA[-1]
a_max_NMC: float = OCP_NMC[-1]

plt.hlines(4.3, 0, 1, colors='red', linestyles='--')
plt.plot(SOC_LCO, OCP_LCO, label="LCO")
plt.plot(SOC_LFP, OCP_LFP, label="LFP")
plt.plot(SOC_LMO, OCP_LMO, label="LMO")
plt.plot(SOC_NCA, OCP_NCA, label="NCA")
plt.plot(SOC_NMC, OCP_NMC, label="NMC")

plt.xlabel("SOC")
plt.ylabel("OCP [V]")

plt.title("OCP of Positive Electrodes at 298.15 K")

plt.legend()
plt.show()
