"""
This module contains example parameters for the battery simulations
"""

import numpy as np

# Positive Electrode
L_p: float = 7.000000e-05
A_p: float = 5.960000e-02
max_conc_p: float = 51410
epsilon_p: float = 0.49
kappa_p: float = 3.8
S_p: float = 1.1167
R_p: float = 8.5e-6
T_ref_p: float = 298.15
D_ref_p: float = 1e-14
k_ref_p: float = 6.67e-11
Ea_D_p: float = 29000
Ea_R_p: float = 58000
brugg_p: float = 1.5
# SOC_init_p: float = 0.59
# SOC_p: float = SOC_init_p
soc_min_p: float = 0.4956 
soc_max_p: float = 0.989011
alpha_p: float = 0.5

# Negative Electrode
# SOC_init_n: float = 0.59
A_n: float = 0.0596
L_n: float = 7.35e-5
kappa_n: float = 100
epsilon_n: float = 0.59
S_n: float = 0.7824
max_conc_n: float = 31833
R_n: float = 12.5e-6
k_ref_n: float = 1.76e-11
D_ref_n: float = 3.9e-14
Ea_R_n: float = 2e4
Ea_D_n: float = 3.5e4
alpha_n: float = 0.5
T_ref_n: float = 298.15
brugg_n: float = 1.5
soc_min_n: float = 0.01890232
soc_max_n: float = 0.7568
alpha_n: float = 0.5

# Electrolyte Parameters
L_e: float = 2e-5
c_init_e: float = 1000.0
kappa_e: float = 0.2875
epsilon_e: float = 0.724
brugg_e: float = 1.5

# Battery Parameters
T: float = 298.15
rho: float = 1626
Vol: float = 3.38e-5
C_p: float = 750
h: float = 1
A: float = 0.085
cap: float = 1.65
V_max: float = 4.2
V_min: float = 2.5
R_cell: float = 0.0028230038442483246

# Simulation parameters
discharge_current: float = 1.5
V_min: float = 2.5
soc_lib_min: float = 0.0
soc_lib: float = 0.0

# functions
def OCP_ref_p(SOC: float) -> float:
    return 4.04596 + np.exp(-42.30027 * SOC + 16.56714) - 0.04880 * np.arctan(50.01833 * SOC - 26.48897) \
              - 0.05447 * np.arctan(18.99678 * SOC - 12.32362) - np.exp(78.24095 * SOC - 78.68074)


def dOCPdT_p(SOC: float) -> float:
    num = -0.19952 + 0.92837*SOC - 1.36455 * SOC ** 2 + 0.61154 * SOC ** 3
    dem = 1 - 5.66148 * SOC + 11.47636 * SOC**2 - 9.82431 * SOC**3 + 3.04876 * SOC**4
    return (num/dem) * 1e-3 # since the original unit are of mV/K


def OCP_ref_n(SOC: float) -> float:
    return 0.13966 + 0.68920 * np.exp(-49.20361 * SOC) + 0.41903 * np.exp(-254.40067 * SOC) \
            - np.exp(49.97886 * SOC - 43.37888) - 0.028221 * np.arctan(22.52300 * SOC - 3.65328) \
            -0.01308 * np.arctan(28.34801 * SOC - 13.43960)


def dOCPdT_n(SOC: float) -> float:
    num = 0.00527 + 3.29927 * SOC - 91.79326 * SOC ** 2 + 1004.91101 * SOC ** 3 - \
          5812.27813 * SOC ** 4 + 19329.75490 * SOC ** 5 - 37147.89470 * SOC ** 6 + \
          38379.18127 * SOC ** 7 - 16515.05308 * SOC ** 8
    dem = 1 - 48.09287 * SOC + 1017.23480 * SOC**2 - 10481.80419 * SOC**3 + \
          59431.30001 * SOC**4 - 195881.64880 * SOC**5 + 374577.31520 * SOC**6 - \
          385821.16070 * SOC**7 + 165705.85970 * SOC**8
    return (num/dem) * 1e-3 # since the original unit are of mV/K