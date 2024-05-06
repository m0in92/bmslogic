import numpy as np
import matplotlib.pyplot as plt

from cpp_modules.solvers import LCO, NMC, LFP, LMO, NCA


electrode_temp = 298.15

SOC_LCO: np.ndarray = np.linspace(0.39, 1)
OCP_LCO: np.ndarray = LCO(soc = SOC_LCO)

SOC_NMC: np.ndarray = np.linspace(0.39, 0.99)
OCP_NMC: np.ndarray = NMC(soc=SOC_NMC)

SOC_LMO: np.ndarray = np.linspace(0.18, 0.95)
OCP_LMO: np.ndarray = LMO(soc=SOC_LMO)

SOC_NCA: np.ndarray = np.linspace(0.19, 1)
OCP_NCA: np.ndarray = NCA(soc=SOC_NCA)

SOC_LFP: np.ndarray = np.linspace(0.05, 1)
OCP_LFP: np.ndarray = LFP(soc=SOC_LFP)

print("LCO OCP when SOC = 0.4: ", LCO(soc=0.4))
print("NMC OCP when SOC = 0.4: ", NMC(soc=0.4))

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



