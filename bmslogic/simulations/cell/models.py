"""
Contains the classes and/or functions that calculate the battery cell model equations (including thermal and degradation models).
"""

from typing import Union
__all__ = ["SPM", "SPMe", "P2DM", "Lumped", "ECMLumped", "ROMSEI"]

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2024 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'

from typing import Union, Callable

import numpy as np
import scipy

from bmslogic.calc_helpers.constants import Constants
from bmslogic.simulations.cell.custom_warnings_exceptions import InvalidElectrodeType
from bmslogic.simulations.cell.battery_components import PyBatteryCell


"""
Below are the models to that calculates the cell terminal voltage.
"""

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'


class PyThevenin1RC:
    """
    This class creates a first order Thevenin model object for a lithium-ion battery cell. It contains relevant model
    parameters as class attributes and methods to calculate SOC and terminal voltage.

    Thevenin first order model is a phenomenological model that can be used to simulate the terminal voltage across a
    lithium-ion battery cell. It has representative electrical components that represent the open-circuit voltage,
    internal resistance, and diffusion voltages. The set of differential and algebraic equations are:

    dz/dt = -eta(t) * i_app(t) / capacity
    di_R1/dt = -i_R1/(R1*C1) + i_app(t)/(R1*C1)
    v(t) = OCV(z(t)) - R1*i_R1(t) - R0*i_app(t)

    Where the second equation is a non-homogenous linear first-order differential equation. Furthermore, the variables
    are:
    z: state of charge (SOC)
    R0: resistance of the resistor that represents the battery cell's internal resistance
    R1: resistance of the resistor in the RC pair.
    C1: capacitance of the capacitor in the RC pair.
    i_R1: current through R1
    i_app: applied current
    eta: Colombic efficiency

    Note that the RC pair represents the diffusion voltage in the battery cell.


    After time discretization, the set of algebraic equations are:

    z[k+1] = z[k] - delta_t*eta[k]*i_app[k]/capacity
    i_R1[k+1] = exp(-delta_t/(R1*C1))*i_R1[k] + (1-exp(-delta_t/(R1*C1))) * i_app[k]
    v[k] = OCV(z[k]) - R1*i_R1[k] - R0*i_app[k]

    Where k represents the time-point and delta_t represents the time-step between z[k+1] and z[k].

    Code Notes:
    1. It is assumed for now that eta is a function of applied current only.
    2. Discharge currrent is positve and charge current is negative by convention.

    Reference:
    Hariharan, K. S. (2013). A coupled nonlinear equivalent circuit – Thermal model for lithium ion cells.
    In Journal of Power Sources (Vol. 227, pp. 171–176). Elsevier BV.
    https://doi.org/10.1016/j.jpowsour.2012.11.044
    """
    @classmethod
    def soc_next(cls, dt: float, i_app: float, SOC_prev: float, Q: float, eta: float):
        """
        This methods calculates the SOC at the next time-step
        :param dt: time difference between the current and previous time steps [s]
        :param i_app: Applied current [A]
        :param SOC_prev: SOC at the previous time step
        :param Q: battery cell capacity [Ahr]
        :param eta: Columbic efficiency
        :return: SOC at the current time step
        """
        return SOC_prev - dt * eta * i_app / (3600 * Q)

    @classmethod
    def i_R1_next(cls, dt: float, i_app: float, i_R1_prev: float, R1: float, C1: float):
        """
        Measures the current through R1 (i_R1) at the current time step.
        :param dt: time difference between the current and the previous time step [s]
        :param i_app: applied current [A]
        :param i_R1_prev: current through the RC branch at the previous time step [A]
        :param R1: resistance of R1 [ohms]
        :param C1: capacitance of C1 [F]
        :return: current through the RC branch at the current time step
        """
        return np.exp(-dt/(R1*C1)) * i_R1_prev + (1-np.exp(-dt/(R1*C1))) * i_app

    @classmethod
    def v(cls, i_app, OCV: float, R0: float, R1: float, i_R1: float):
        """
        This method calculates the cell terminal voltage.
        :param i_app: (float) applied current at current time step, k
        :return: (float) terminal voltage at the current time step, k
        """
        return OCV - R1 * i_R1 - R0 * i_app


class PyESC:
    """
    Class oject contains the relevant functions to perform the Enhanched-self-correcting ECM model.
    Notes:
        The discharge current is assumed to be positive values. Meanwhile, the charge current is negative by convention.
    """

    @classmethod
    def sign(cls, num: Union[int, float]) -> int:
        if num < 0:
            return -1
        elif num == 0:
            return 0
        else:
            return 1

    @classmethod
    def s(cls, i_app: float, s_prev: float) -> float:
        """
        Returns the value for the instantaneous hysteresis
        :param i_app: Applied battery cell current [A]
        :return: value for the instantaneous hysteresis
        """
        if abs(i_app) > 0:
            return PyESC.sign(num=i_app)
        else:
            return s_prev

    @classmethod
    def soc_next(cls, dt: float, i_app: float, SOC_prev: float, Q: float, eta: float):
        """
        This methods calculates the SOC at the next time-step
        :param dt: time difference between the current and previous time steps [s]
        :param i_app: Applied current [A]
        :param SOC_prev: SOC at the previous time step
        :param Q: battery cell capacity [Ahr]
        :param eta: Columbic efficiency
        :return: SOC at the current time step
        """
        return PyThevenin1RC.soc_next(dt=dt, i_app=i_app, SOC_prev=SOC_prev, Q=Q, eta=eta)

    @classmethod
    def i_R1_next(cls, dt: float, i_app: float, i_R1_prev: float, R1: float, C1: float):
        """
        Measures the current through R1 (i_R1) at the current time step.
        :param dt: time difference between the current and the previous time step [s]
        :param i_app: applied current [A]
        :param i_R1_prev: current through the RC branch at the previous time step [A]
        :param R1: resistance of R1 [ohms]
        :param C1: capacitance of C1 [F]
        :return: current through the RC branch at the current time step
        """
        return PyThevenin1RC.i_R1_next(dt=dt, i_app=i_app, i_R1_prev=i_R1_prev, R1=R1, C1=C1)

    @classmethod
    def h_next(cls, dt: float, i_app: float, eta: float, gamma: float, cap: float, h_prev: float) -> float:
        exp_term = np.exp(-np.abs((eta * i_app * gamma * dt) / (3600 * cap)))
        return exp_term * h_prev - (1 - exp_term) * PyESC.sign(i_app)

    @classmethod
    def v(cls, i_app, ocv: float, R0: float, R1: float, i_R1: float,
          m_0: float, m: float, h: float, s_prev: float) -> float:
        return ocv - R1 * i_R1 - R0 * i_app + m * h + m_0 * PyESC.s(i_app=i_app, s_prev=s_prev)


class PySPM:
    """
    This class contains the methods for calculating the molar lithium flux, cell terminal voltage according to the
    single particle model.
    """

    @classmethod
    def molar_flux_electrode(cls, I: float, S: float, electrode_type: str) -> float:
        """
        Calculates the model lithium-ion flux [mol/m2/s] into the electrodes.
        :param I: (float) Applied current [A]
        :param S: (float) electrode electrochemically active area [m2]
        :param electrode_type: (str) positive electrode ('p') or negative electrode ('n')
        :return: (float) molar flux [mol/m2/s]
        """
        if electrode_type == 'p':
            return I / (Constants.F * S)
        elif electrode_type == 'n':
            return -I / (Constants.F * S)
        else:
            raise InvalidElectrodeType

    @staticmethod
    def flux_to_current(molar_flux: float, S: float, electrode_type: str) -> float:
        """
        Converts molar flux [mol/m2/s] to current [A].
        :param molar_flux: molar lithium-ion flux [mol/m2/s]
        :param S: (float) electrode electrochemically active area [m2]
        :param electrode_type: (str) positive electrode ('p') or negative electrode ('n')
        :return: (float) current [A]
        """
        if electrode_type == 'p':
            return molar_flux * Constants.F * S
        elif electrode_type == 'n':
            return -molar_flux * Constants.F * S
        else:
            raise InvalidElectrodeType

    @staticmethod
    def m(I: float, k: float, S: float, c_max: float, SOC: float, c_e: float) -> float:
        return I / (Constants.F * k * S * c_max * (c_e ** 0.5) * ((1 - SOC) ** 0.5) * (SOC ** 0.5))

    @staticmethod
    def calc_cell_terminal_voltage(OCP_p: float, OCP_n: float, m_p: float, m_n: float, R_cell: float,
                                   T: float, I: float) -> tuple[float, float, float, float, float]:
        OCV: float = OCP_p - OCP_n
        overpotential_elec_p: float = (
            2 * Constants.R * T / Constants.F) * np.log((np.sqrt(m_p ** 2 + 4) + m_p) / 2)
        overpotential_elec_n: float = (
            2 * Constants.R * T / Constants.F) * np.log((np.sqrt(m_n ** 2 + 4) + m_n) / 2)
        overpotential_R_cell: float = I * R_cell
        # V = OCP_p - OCP_n
        # V += (2 * Constants.R * T / Constants.F) * \
        #     np.log((np.sqrt(m_p ** 2 + 4) + m_p) / 2)
        # V += (2 * Constants.R * T / Constants.F) * \
        #     np.log((np.sqrt(m_n ** 2 + 4) + m_n) / 2)
        # V += I * R_cell
        V: float = OCV + overpotential_elec_p + \
            overpotential_elec_n + overpotential_R_cell
        return V, OCV, overpotential_elec_p, overpotential_elec_n, overpotential_R_cell

    def __call__(self, OCP_p: float, OCP_n: float, R_cell: float,
                 k_p: float, S_p: float, c_smax_p: float, SOC_p: float,
                 k_n: float, S_n: float, c_smax_n: float, SOC_n: float,
                 c_e: float,
                 T: float, I_p_i: float, I_n_i: float) -> tuple[float, float, float, float, float]:
        """
        Calculates the cell terminal voltage and other overpotential contributions.
        :param OCP_p: Open-circuit potential of the positive electrode [V]
        :param OCP_n: Open-circuit potential of the negative electrode [V]
        :param R_cell: Battery cell ohmic resistance [ohms]
        :param k_p: positive electrode rate constant [m2 mol0.5 / s]
        :param S_p:  positive electrode electro-active area [mol/m2]
        :param c_smax_p: positive electrode max. lithium conc. [mol]
        :param SOC_p: positive electrode SOC
        :param k_n: negative electrode rate constant [m2 mol0.5 / s]
        :param S_n: negative electrode electrochemical active area [m2/mol]
        :param c_smax_n: negative electrode max. lithium conc. [mol]
        :param SOC_n: negative electrode SOC
        :param c_e: electrolyte conc. [mol]
        :param T: Battery cell temperature [K]
        :param I_p_i: positive electrode intercalation applied current [A]
        :param I_n_i: negative electrode intercalation applied current [A]
        :return: Battery cell terminal voltage [V]
        """
        m_p: float = self.m(I=I_p_i, k=k_p, S=S_p,
                            c_max=c_smax_p, SOC=SOC_p, c_e=c_e)
        m_n: float = self.m(I=I_n_i, k=k_n, S=S_n,
                            c_max=c_smax_n, SOC=SOC_n, c_e=c_e)
        return self.calc_cell_terminal_voltage(OCP_p=OCP_p, OCP_n=OCP_n, m_p=m_p, m_n=m_n, R_cell=R_cell, T=T, I=I_p_i)


class PySPMe:
    """
    This class contains the methods to calculate the molar ionic flux in the electrode regions and the cell terminal
    voltage as expressed in the SPMe model [1].

    Reference:
    [1] S. J. Moura, F. B. Argomedo, R. Klein, A. Mirtabatabaei and M. Krstic,
    "Battery State Estimation for a Single Particle Model With Electrolyte Dynamics,"
    in IEEE Transactions on Control Systems Technology, vol. 25, no. 2, pp. 453-468, March 2017,
    doi: 10.1109/TCST.2016.2571663.
    """

    @classmethod
    def molar_flux_electrode(cls, I: float, S: float, electrode_type: str) -> float:
        """
        Returns the area molar flux entering/exiting the electrode surface [mol/m2/s]
        :param I:
        :param S:
        :param electrode_type:
        :return:
        """
        if electrode_type == 'p':
            return I / (Constants.F * S)
        elif electrode_type == 'n':
            return -I / (Constants.F * S)
        else:
            raise InvalidElectrodeType

    @classmethod
    def a_s(cls, epsilon: float, R: float) -> float:
        """
        Calculates the electrode's interfacial surface area [m2/m3]
        :param epsilon: active material volume fraction
        :param R: radius of the electrode particle
        :return: (float) electrode's interfacial surface area [m2/m3]
        """
        return 3 * epsilon / R

    @classmethod
    def i_0(cls, k: float, c_s_max: float, c_e: float, soc_surf: float) -> float:
        """
        Calculates the exchange current density for an electrode [mol/m2/s].
        :param k: rate constant [m2.5 / mol0.5 / s]
        :param c_s_max: max. lithium-ion electrode conc. [mol/m3]
        :param c_e: lithium-ion conc in the electrolyte [mol/m3]
        :param SOC_surf: state-of-charge of the electrode particle surface
        :return: (float) exchange current density [mol/m2/s]
        """
        return k * c_s_max * (c_e ** 0.5) * ((1 - soc_surf) ** 0.5) * (soc_surf ** 0.5)

    @classmethod
    def m(cls, i_app: float, k: float, S: float, c_s_max: float, c_e: float, soc_surf: float) -> float:
        return i_app / (Constants.F * S * PySPMe.i_0(k=k, c_s_max=c_s_max, c_e=c_e, soc_surf=soc_surf))

    @classmethod
    def calc_terminal_voltage(cls, ocp_p: float, ocp_n: float, m_p: float, m_n: float,
                              l_p: float, l_sep: float, l_n: float,
                              kappa_eff_avg: float, k_f_avg: float, t_c: float,
                              R_cell: float,
                              c_e_n: float, c_e_p: float,
                              temp: float, i_app: float) -> float:
        """
        Returns the cell terminal voltage [V] according to Moura et al.
        Note that the charge and the discharge currents are denoted with a positive and negative numbers, respectively.
        :param ocp_p:
        :param ocp_n:
        :param m_p:
        :param m_n:
        :param l_p:
        :param l_sep:
        :param l_n:
        :param battery_cross_area:
        :param kappa_eff_avg:
        :param k_f_avg:
        :param t_c:
        :param R_cell:
        :param c_e_n:
        :param c_e_p:
        :param temp:
        :param i_app:
        :return:
        """
        k_conc: float = (2 * Constants.R * temp /
                         Constants.F) * (1 - t_c) * k_f_avg

        V: float = ocp_p - ocp_n
        V += (2 * Constants.R * temp / Constants.F) * \
            np.log((np.sqrt(m_p ** 2 + 4) + m_p) / 2)
        V += (2 * Constants.R * temp / Constants.F) * \
            np.log((np.sqrt(m_n ** 2 + 4) + m_n) / 2)
        V += R_cell * i_app
        V += (l_p + 2 * l_sep + l_n) * i_app / (2 * kappa_eff_avg)
        V += k_conc * (np.log(c_e_p) - np.log(c_e_n))
        return V

    @classmethod
    def calc_overpotentials(cls, ocp_p: float, ocp_n: float, m_p: float, m_n: float,
                            l_p: float, l_sep: float, l_n: float,
                            kappa_eff_avg: float, k_f_avg: float, t_c: float,
                            R_cell: float,
                            c_e_n: float, c_e_p: float,
                            temp: float, i_app: float) -> tuple[float, float, float, float, float, float]:
        k_conc: float = (2 * Constants.R * temp /
                         Constants.F) * (1 - t_c) * k_f_avg

        OCV: float = ocp_p - ocp_n
        overpotential_elec_p: float = (
            2 * Constants.R * temp / Constants.F) * np.log((np.sqrt(m_p ** 2 + 4) + m_p) / 2)
        overpotential_elec_n: float = (
            2 * Constants.R * temp / Constants.F) * np.log((np.sqrt(m_n ** 2 + 4) + m_n) / 2)
        overpotential_R_cell: float = R_cell * i_app
        overpotential_electrolyte: float = (
            l_p + 2 * l_sep + l_n) * i_app / (2 * kappa_eff_avg)
        overpotential_electrolyte += k_conc * (np.log(c_e_p) - np.log(c_e_n))
        V: float = OCV + overpotential_elec_p + overpotential_elec_n + \
            overpotential_R_cell + overpotential_electrolyte
        return V, OCV, overpotential_elec_p, overpotential_elec_n, overpotential_R_cell, overpotential_electrolyte

    def __call__(self, ocp_p: float, ocp_n: float, R_cell: float,
                 k_p: float, S_p: float, c_smax_p: float, soc_surf_p: float,
                 k_n: float, S_n: float, c_smax_n: float, soc_surf_n: float,
                 c_e: float,
                 temp: float, I_p_i: float, I_n_i: float,
                 l_p: float, l_sep: float, l_n: float,
                 kappa_eff_avg: float, k_f_avg: float, t_c: float,
                 c_e_n: float, c_e_p: float) -> tuple[float, float, float, float, float, float]:
        m_p: float = self.m(i_app=I_p_i, k=k_p, S=S_p,
                            c_s_max=c_smax_p, soc_surf=soc_surf_p, c_e=c_e)
        m_n: float = self.m(i_app=I_n_i, k=k_n, S=S_n,
                            c_s_max=c_smax_n, soc_surf=soc_surf_n, c_e=c_e)

        V, OCV, overpotential_elec_p, overpotential_elec_n, overpotential_R_cell, overpotential_electrolyte = self.calc_overpotentials(ocp_p=ocp_p, ocp_n=ocp_n, m_p=m_p, m_n=m_n,
                                                                                                                                       l_p=l_p, l_sep=l_sep, l_n=l_n,
                                                                                                                                       kappa_eff_avg=kappa_eff_avg, k_f_avg=k_f_avg, t_c=t_c,
                                                                                                                                       R_cell=R_cell,
                                                                                                                                       c_e_n=c_e_n, c_e_p=c_e_p,
                                                                                                                                       temp=temp, i_app=I_n_i)

        return V, OCV, overpotential_elec_p, overpotential_elec_n, overpotential_R_cell, overpotential_electrolyte


class PyP2DM:
    """
    Contains class methods that calculate the general equations pertaining to the P2D Model.
    """

    @classmethod
    def a_s(cls, epsilon, r) -> float:
        """
        Calculates the specific interfacial surface area [m] of an solid electrode phase
        :param epsilon: Volume fraction of the active material in the solid electrode phase
        :param r: the radius of the electrode particle [m]
        :return: (float) specific interfacial surface area [m]
        """
        return 3 * epsilon / r

    @classmethod
    def i_0(cls, k: Union[float, np.ndarray],
            c_s_surf: Union[float, np.ndarray], c_s_max: float,
            c_e: Union[float, np.ndarray],
            c_e_0: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        return Constants.F * k * ((c_s_max - c_s_surf) ** 0.5) * (c_s_surf ** 0.5) * (c_e / c_e_0) ** 0.5

    @classmethod
    def v_n_minus_v_e(cls, array_i_0_n: np.ndarray, array_eta_rel_n: np.ndarray, array_coord_n: np.ndarray,
                      i_app: float, temp: float, a_s_n: float, cell_area: float, L_n: float) -> np.ndarray:
        func_i_0 = scipy.interpolate.interp1d(
            array_coord_n, array_i_0_n, fill_value='extrapolate')
        func_rel_eta_n = scipy.interpolate.interp1d(
            array_coord_n, array_eta_rel_n, fill_value='extrapolate')

        def func_integrand1(x) -> float:
            return func_i_0(x) * np.exp(Constants.F * func_rel_eta_n(x) / (2 * Constants.R * temp))

        def func_integrand2(x: float) -> float:
            return func_i_0(x) * np.exp(-Constants.F * func_rel_eta_n(x) / (2 * Constants.R * temp))

        coeff = 2 * Constants.R * temp / Constants.F  # coefficient
        term1 = -i_app / cell_area
        term2 = a_s_n * scipy.integrate.quad(func_integrand1, 0, L_n)[0]
        term3 = a_s_n * scipy.integrate.quad(func_integrand2, 0, L_n)[0]
        return coeff * np.log((term1 + (term1 ** 2 + (4 * term2 * term3)) ** 0.5) / (2 * a_s_n * term2))

    @classmethod
    def v_p_minus_v_e(cls, array_i_0_p: np.ndarray, array_eta_rel_p: np.ndarray, array_coord_p: np.ndarray,
                      i_app: float, temp: float, a_s_p: float, cell_area: float, L_p_0: float, L_p: float):
        func_i_0_p = scipy.interpolate.interp1d(
            array_coord_p, array_i_0_p, fill_value='extrapolate')
        func_eta_rel_p = scipy.interpolate.interp1d(
            array_coord_p, array_eta_rel_p, fill_value='extrapolate')

        def integrand1(x: float) -> float:
            return func_i_0_p(x) * np.exp(Constants.F * func_eta_rel_p(x) / (2 * Constants.R * temp))

        def integrand2(x: float) -> float:
            return func_i_0_p(x) * np.exp(-Constants.F * func_eta_rel_p(x) / (2 * Constants.R * temp))

        coeff = 2 * Constants.R * temp / Constants.F
        term1 = -i_app / cell_area
        term2 = a_s_p * \
            scipy.integrate.quad(func=integrand1, a=L_p_0, b=L_p)[0]
        term3 = a_s_p * \
            scipy.integrate.quad(func=integrand2, a=L_p_0, b=L_p)[0]
        return coeff * np.log((term1 + (term1**2 + 4*term2*term3)**0.5) / (2 * a_s_p * term2))

    @classmethod
    def v_p(cls):
        pass

    @classmethod
    def calc_eta_from_rel_eta(cls, rel_eta: np.ndarray, v_terminal: float, v_terminal_e: float) -> np.ndarray:
        return rel_eta + v_terminal - v_terminal_e

    @classmethod
    def calc_j_from_BV(cls, i_0: Union[float, np.ndarray], eta: Union[float, np.ndarray],
                       temp: float) -> Union[float, np.ndarray]:
        exp_term = 0.5 * Constants.F * eta / (Constants.R * temp)
        return (i_0/Constants.F) * (np.exp(exp_term) - np.exp(-exp_term))


"""
Below are the thermal models
"""


class PyLumped:
    def __init__(self, b_cell: PyBatteryCell):
        # check for input arguments
        if not isinstance(b_cell, PyBatteryCell):
            raise TypeError(
                "b_cell input argument needs to be a BatteryCell object.")
        # Assign class atributes
        self.b_cell = b_cell

    def reversible_heat(self, I: float, T: float) -> float:
        return I * T * (self.b_cell.elec_p.dOCPdT - self.b_cell.elec_n.dOCPdT)

    def irreversible_heat(self, I: float, V: float) -> float:
        return I * (V - (self.b_cell.elec_p.OCP - self.b_cell.elec_n.OCP))

    def heat_flux(self, T: float) -> float:
        return self.b_cell.h * self.b_cell.A * (T - self.b_cell.T_amb)

    def heat_balance(self, V: float, I: float) -> Callable:
        def func_heat_balance(T: float, t: float) -> float:
            main_coeff = 1 / (self.b_cell.rho *
                              self.b_cell.Vol * self.b_cell.C_p)
            return main_coeff * (self.reversible_heat(I=I, T=T) + self.irreversible_heat(I=I, V=V) - self.heat_flux(T=T))
        return func_heat_balance


class PyECMLumped:
    def reversible_heat(self, I: float, T: float, dOCVdT: float) -> float:
        return I * T * dOCVdT

    def irreversible_heat(self, I: float, V: float, OCV: float) -> float:
        return I * (V - OCV)

    def heat_flux(self, T: float, h: float, A: float, T_amb: float):
        return h * A * (T - T_amb)

    def heat_balance(self, V: float, I: float, rho: float, Vol: float, C_p: float,
                     OCV: float, dOCVdT: float, h: float, A: float, T_amb: float) -> Callable:
        def func_heat_balance(T: float, t: float) -> float:
            main_coeff: float = 1 / (rho * Vol * C_p)
            return main_coeff * (self.reversible_heat(I=I, T=T, dOCVdT=dOCVdT) +
                                 self.irreversible_heat(I=I, V=V, OCV=OCV) -
                                 self.heat_flux(T=T, h=h, A=A, T_amb=T_amb))
        return func_heat_balance


"""
Below are the battery cell degradation model equations
"""


class PyROMSEI:
    """
    This class contains the equations for the reduced order SEI growth model as mentioned in ref [1], with slight
    modifications.

    Literature Reference:
    1. Randell et al. "Controls oriented reduced order modeling of solid-electrolyte interphase layer growth". 2012.
    Journal of Power Sources. Vol: 209. pgs: 282-288.
    """

    @classmethod
    def calc_j_0_i(cls, k: float, c_s_max: float, c_e: float, soc: float) -> float:
        """
        Calculates the exchange lithium ion flux density [mol/m2/s]
        :param k: rate of reaction at the negative electrode [m2.5/mol-0.5/s]
        :param c_s_max: max. lithium concentration at the negative electrode [mol/m3]
        :param c_e: electrolyte concentration [mol/m3]
        :param soc: negative electrode SOC
        :return: (float) exchange current density [mol/m2/s]
        """
        return k * c_s_max * (c_e ** 0.5) * ((1-soc) ** 0.5) * soc ** 0.5

    @classmethod
    def calc_j_tot(cls, I: float, S: float) -> float:
        return PySPM.molar_flux_electrode(I=I, S=S, electrode_type='n')

    @classmethod
    def calc_j_i(cls, j_tot: float, j_s: float) -> float:
        return j_tot - j_s

    @classmethod
    def calc_eta_n(cls, temp: float, j_i: float, j_0_i: float) -> float:
        """
        Calculates and returns the surface over-potential [V] of the intercalation reaction.
        :param temp: Electrode temperature [K]
        :param j_i: intercalation flux [mol/m2/s]
        :param j_0_i: intercalation reaction exchange current [mol/m2/s]
        :return: (float) intercalation reaction surface over-potential [V]
        """
        return (2 * Constants.R * temp / Constants.F) * (np.arcsinh(j_i / (2 * j_0_i)))

    @classmethod
    def calc_eta_s(cls, eta_n: float, ocp_n: float, ocp_s: float) -> float:
        """
        Calculates and returns the side-reaction electrode surface over-potential [V]
        :param eta_n: intercalation reaction over-potential [V]
        :param ocp_n: open-circuit potential of the electrode [V
        :param ocp_s: reference potential of the SEI side reaction [V]
        :return:
        """
        return eta_n + ocp_n - ocp_s

    @classmethod
    def calc_j_s(cls, temp: float, j_0_s: float, eta_s: float) -> float:
        """
        Calculates and returns the side-reaction flux [mol/m2/s]
        :param temp: Electrode temperature [K]
        :param j_0_s: side reaction exchange current density [mol/m2/s]
        :param eta_s: side reaction surface over-potential [V]
        :return: (float) side reaction flux [mol/m2/s]
        """
        return -j_0_s * np.exp(-Constants.F * eta_s / (2 * Constants.R * temp))

    @classmethod
    def flux_to_current(cls, molar_flux: float, S: float) -> float:
        """
        Converts molar flux [mol/m2/s] to current [A].
        :param molar_flux: molar lithium-ion flux [mol/m2/s]
        :param S: (float) electrode electrochemically active area [m2]
        :return: current [A]
        """
        return PySPM.flux_to_current(molar_flux=molar_flux, S=S, electrode_type='n')
