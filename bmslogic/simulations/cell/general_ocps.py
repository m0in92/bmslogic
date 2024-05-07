"""
Contains the functions for the positive and negative electode's OCP as found in Schmit et al.

Note that the electrode temperatures are assumed to be at 298.15 K.

Reference:
Schmitt, J., Schindler, M., & Jossen, A. (2021). Change in the half-cell open-circuit potential curves of
silicon–graphite and nickel-rich lithium nickel manganese cobalt oxide during cycle aging.
Journal of Power Sources, 506, 230240. https://doi.org/10.1016/J.JPOWSOUR.2021.230240

Guo, M., Sikha, G., & White, R. E. (2011). Single-Particle Model for a Lithium-Ion Cell: Thermal Behavior.
Journal of The Electrochemical Society, 158(2), A122. https://doi.org/10.1149/1.3521314/XML
"""

__all__ = ["calc_ocp_schmit", "LCO", "NMC", "LFP", "LMO", "NCA",
           "MCMB", "PetroleumCoke", "HardCarbon", "LTO", "graphite"]

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All rights reserved."
__status__ = "deployed"

from typing import Union

import numpy as np

from bmslogic.calc_helpers.constants import Constants


def calc_ocp_schmit(A_list: list, K: float, U0: float, x: float) -> float:
    R: float = Constants.R
    F: float = Constants.F
    T: float = 298.15

    # second term
    sec_term = (R * T / F) * np.log((1 - x) / x)

    # third term
    pre_term = 1 / (K * (2 * x - 1) + 1) ** 2
    post_term = 0
    for i, A in enumerate(A_list):
        post_term += (A / F) * ((2 * x - 1) ** (i + 1) - 2 *
                                i * x * (1 - x) / (2 * x - 1) ** (1 - i))
    third_term = pre_term * post_term

    # fourth term
    post_term = 0
    for i, A in enumerate(A_list):
        post_term += (A / F) * ((2 * x - 1) ** i) * \
            (2 * (i + 1) * (x ** 2) - 2 * (i + 1) * x + 1)
    fou_term = K * post_term

    return U0 + sec_term + third_term + fou_term


def LCO(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [5166082.0, -5191279.0, 5232986.0, -5257083.0, 5010583.0, -4520614.0, 7306952.0, -14634260.0,
                    6705611.0,
                    33894160.0, -63528110.0, 30487930.0, 21440020.0, -27731990.0, 8206452.0]
    K = -2.369020e-04
    U0: float = -2.276828e+01
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def NMC(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        -1306.411,
        -57995.21,
        128590.6,
        -141860.5,
        128196.9,
        -328128.3,
        817.6398,
        1373879,
        651141.4,
        -7315831,
        4983891,
        6925178,
        -6123714,
        -3595215,
        3340694
    ]
    K: float = -0.635961
    U0: float = 3.755472
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def LFP(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        -2244.923,
        -2090.675,
        -6045.274,
        -6046.354,
        -13952.1,
        49285.95,
        57688.95,
        -270619.6,
        -262397.3,
        695491.2,
        480539,
        -881803.7,
        -450067.5,
        425577.8,
        127814.6
    ]
    K: float = 0.03932999
    U0: float = 3.407141
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def LMO(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        28.88073,
        -19289.65,
        27516.93,
        25997.59,
        47959.29,
        -277348.8,
        -321162.5,
        998439.1,
        1227530,
        -2722189,
        -1973511,
        4613775,
        818839.4,
        -4157314,
        1709075
    ]
    K: float = -0.9996536
    U0: float = 4.004463
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def NCA(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        1545979,
        -1598187,
        1595170,
        -1605545,
        1521194,
        -1645695,
        1809373,
        -1578053,
        2032672,
        -2281842,
        -1678912,
        2858489,
        5443521,
        -9459781,
        3600413
    ]
    K: float = 0.000104664
    U0: float = -4.419803
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def MCMB(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        1115.732,
        -114405.2,
        -98955.51,
        -84726.47,
        -267608.3,
        -476169.2,
        603250.8,
        1867866,
        -1698309,
        -5707850,
        873999.3,
        7780654,
        1486486,
        -4703010,
        -2275145]
    K: float = 1.000052
    U0: float = -0.4894122
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def PetroleumCoke(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        3257341,
        3324795,
        3293786,
        3305070,
        3341687,
        3286297,
        2786389,
        2943793,
        6028857,
        8242393,
        1365959,
        -10369090,
        -13287330,
        -6890890,
        -1366119]
    K: float = 1.02E-05
    U0: float = 17.37471
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def HardCarbon(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        643.3323,
        92777.34,
        120803.9,
        39097.09,
        70427.33,
        452782.1,
        925998.1,
        111.1642,
        -1853447,
        -323266.3,
        3899277,
        2862780,
        -2837527,
        -4199996,
        -1406372]
    K: float = 0.9896854
    U0: float = 0.5839445
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def LTO(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    # # function calculations
    A_list: list = [
        -2730.278,
        5232.911,
        -8075.451,
        -4993.786,
        36438.75,
        110508.7,
        -361370.2,
        -502525.3,
        1401392,
        1148841,
        -2857197,
        -1211581,
        2819998,
        479102.9,
        -1091785]
    K: float = 0.1291628
    U0: float = 1.596152
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def graphite(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Obtained from Guo et al.
    :param soc: electrode state of charge
    :return: electrode open-circuit potential [V]

    Reference:
    Guo, M., Sikha, G., & White, R. E. (2011). Single-Particle Model for a Lithium-Ion Cell: Thermal Behavior.
    Journal of The Electrochemical Society, 158(2), A122. https://doi.org/10.1149/1.3521314/XML
    """
    return 0.13966 + 0.68920 * np.exp(-49.20361 * soc) + 0.41903 * np.exp(-254.40067 * soc) \
        - np.exp(49.97886 * soc - 43.37888) - 0.028221 * np.arctan(22.52300 * soc - 3.65328) \
        - 0.01308 * np.arctan(28.34801 * soc - 13.43960)
