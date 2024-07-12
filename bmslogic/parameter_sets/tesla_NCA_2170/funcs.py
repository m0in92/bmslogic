"""
Contains the functions for the open-circuit potentials of the electrode.
"""
__author__ = "Moin Ahmed"

from typing import Union

import numpy as np
import numpy.typing as npt



def ocp_p(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    co_eff: np.ndarray = np.array([-2.22458893e+03, 9.42883013e+03, -1.49421424e+04, 9.30181481e+03,
                                   1.32800790e+03, -5.11625286e+03, 2.77757968e+03, -5.67585212e+02,
                                   2.82091663e+00, 1.21754506e+01, -1.59354658e+00, 4.24387562e+00])
    return np.polyval(co_eff, soc)

def docpdT_p(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    coeff: np.ndarray = np.array(
        [-36.2797735, 114.845612, -61.0391959, -216.345537, 439.70208, -378.213227, 178.64472, -47.5684336,
         6.63342923, -0.37800454, -0.00453340223, 0.00238263722])
    return np.polyval(coeff, soc)


def OCP_ref_n(SOC):
    return 0.13966 + 0.68920 * np.exp(-49.20361 * SOC) + 0.41903 * np.exp(-254.40067 * SOC) \
            - np.exp(49.97886 * SOC - 43.37888) - 0.028221 * np.arctan(22.52300 * SOC - 3.65328) \
            -0.01308 * np.arctan(28.34801 * SOC - 13.43960)


def dOCPdT_n(SOC):
    num = 0.00527 + 3.29927 * SOC - 91.79326 * SOC ** 2 + 1004.91101 * SOC ** 3 - \
          5812.27813 * SOC ** 4 + 19329.75490 * SOC ** 5 - 37147.89470 * SOC ** 6 + \
          38379.18127 * SOC ** 7 - 16515.05308 * SOC ** 8
    dem = 1 - 48.09287 * SOC + 1017.23480 * SOC**2 - 10481.80419 * SOC**3 + \
          59431.30001 * SOC**4 - 195881.64880 * SOC**5 + 374577.31520 * SOC**6 - \
          385821.16070 * SOC**7 + 165705.85970 * SOC**8
    return (num/dem) * 1e-3 # since the original unit are of mV/K


# def func_D_e(c_e: Union[float, npt.ArrayLike], temp: float) -> float:
#     """
#     Calculates the lithium-ion diffusivity in the electrolyte as a func of lithium-ion concentration and temperature
#     Reference: Han et al. A numerically efficient method for solving the full-order pseudo-2D Li-ion cell model.
#     2021. Journal of Power Sources. 490

#     :param c_e: lithium-ion concentration [mol/m3]
#     :param temp: electrolyte temp [K]
#     :return: (float) diffusivity of the lithium-ion [m2/s]
#     """
#     c_e = 0.001 * c_e  # in the original work the concentration was in mol/l
#     return (10 ** (-4.43 - 54 / (temp - (229+5*c_e)) - 0.22 * c_e)) * 1e-4  # the original D_e was in cm2/s


# def func_kappa_e(c_e: Union[float, npt.ArrayLike], temp: float) -> Union[float, npt.ArrayLike]:
#     """
#     Calculates the conductivity [S/m] for the electrolyte.
#     Reference: Han et al. A numerically efficient method for solving the full-order pseudo-2D Li-ion cell model.
#     2021. Journal of Power Sources. 490

#     :param c_e:
#     :param temp:
#     :return:
#     """
#     c_e = c_e * 0.001  # Original work used the units of mol/l for the concentrations
#     kappa_e_ = c_e * (
#                 -10.5 + 0.074 * temp - 6.96e-5 * (temp ** 2) + 0.668 * c_e - 0.0178 * c_e * temp + 2.8e-5 * c_e * (
#                     temp ** 2) + 0.494 * (c_e ** 2) - \
#                 8.86e-4 * (c_e ** 2) * temp) ** 2
#     return kappa_e_ * 1e-3 * 100  # Original work used the units of mS/cm for the conductivity


# def func_dlnf(c_e: Union[float, npt.ArrayLike], temp: float, t_c: float) -> Union[float, npt.ArrayLike]:
#     """
#     Calculates the expression 1+dlnf/dlnc_e

#     Reference: Han et al. A numerically efficient method for solving the full-order pseudo-2D Li-ion cell model.
#     2021. Journal of Power Sources. 490
#     :param c_e:
#     :param temp:
#     :param t_c:
#     :return:
#     """
#     c_e = c_e * 0.001
#     return (0.601-0.24*c_e+(0.982-5.1064e-3*(temp-294.15))*c_e**1.5)/(1-t_c)


