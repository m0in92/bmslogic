import pathlib
import sys
import unittest

import numpy as np

import bmslogic.simulations.cell.Debug.cell as bc


# functions


class testElectrode(unittest.TestCase):
    L = 7.000000e-05
    A = 5.960000e-02
    max_conc = 51410
    epsilon = 0.49
    kappa = 3.8
    S = 1.1167
    R = 8.5e-6
    T_ref = 298.15
    D_ref = 1e-14
    k_ref = 6.67e-11
    Ea_D = 29000  # in J/mol
    Ea_R = 58000  # in J/mol
    brugg = 1.5
    T = 298.15
    SOC_init = 0.59
    SOC = SOC_init
    soc_min, soc_max = 0.4956, 0.989011
    electrode_type = 'none'

    def OCP_ref_p(SOC: float) -> float:
        return 4.04596 + np.exp(-42.30027 * SOC + 16.56714) - 0.04880 * np.arctan(50.01833 * SOC - 26.48897) \
            - 0.05447 * np.arctan(18.99678 * SOC - 12.32362) - \
            np.exp(78.24095 * SOC - 78.68074)


    def dOCPdT_p(SOC: float) -> float:
        num = -0.19952 + 0.92837*SOC - 1.36455 * SOC ** 2 + 0.61154 * SOC ** 3
        dem = 1 - 5.66148 * SOC + 11.47636 * SOC**2 - 9.82431 * SOC**3 + 3.04876 * SOC**4
        return (num/dem) * 1e-3  # since the original unit are of mV/K


    def OCP_ref_n(SOC: float) -> float:
        return 0.13966 + 0.68920 * np.exp(-49.20361 * SOC) + 0.41903 * np.exp(-254.40067 * SOC) \
            - np.exp(49.97886 * SOC - 43.37888) - 0.028221 * np.arctan(22.52300 * SOC - 3.65328) \
            - 0.01308 * np.arctan(28.34801 * SOC - 13.43960)


    def dOCPdT_n(SOC: float) -> float:
        num = 0.00527 + 3.29927 * SOC - 91.79326 * SOC ** 2 + 1004.91101 * SOC ** 3 - \
            5812.27813 * SOC ** 4 + 19329.75490 * SOC ** 5 - 37147.89470 * SOC ** 6 + \
            38379.18127 * SOC ** 7 - 16515.05308 * SOC ** 8
        dem = 1 - 48.09287 * SOC + 1017.23480 * SOC**2 - 10481.80419 * SOC**3 + \
            59431.30001 * SOC**4 - 195881.64880 * SOC**5 + 374577.31520 * SOC**6 - \
            385821.16070 * SOC**7 + 165705.85970 * SOC**8
        return (num/dem) * 1e-3  # since the original unit are of mV/K
    
    # electrode: bc.Electrode = bc.Electrode()

    electrode: bc.Electrode = bc.Electrode(
        L=L, A=A, kappa=kappa, epsilon=epsilon, max_conc=max_conc, R=R, S=S,
        T_ref=T_ref, D_ref=D_ref, k_ref=k_ref, Ea_D=Ea_D, Ea_R=Ea_R, alpha=0.5,
        brugg=brugg, SOC=SOC, T=T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)

    # def test_properties(self) -> None:
    #     electrode: bc.Electrode = bc.Electrode(L=self.L, A=self.A, kappa=self.kappa, epsilon=self.epsilon, max_conc=self.max_conc, R=self.R, S=self.S,
    #                                            T_ref=self.T_ref, D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R, alpha=0.5,
    #                                            brugg=self.brugg, SOC=self.SOC, T=self.T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)

    #     self.assertAlmostEqual(self.T, electrode.T)
    #     self.assertAlmostEqual(self.SOC, electrode.soc)
    #     self.assertAlmostEqual(self.A, electrode.A)
    #     self.assertAlmostEqual(self.S, electrode.S)
    #     self.assertAlmostEqual(self.max_conc, electrode.c_max)

    # def test_method_get_D(self):
    #     temp_new1: float = 313.15  # [K]
    #     temp_new2: float = 273.15  # [K]
    #     electrode: bc.Electrode = bc.Electrode(L=self.L, A=self.A, kappa=self.kappa, epsilon=self.epsilon, max_conc=self.max_conc, R=self.R, S=self.S,
    #                                            T_ref=self.T_ref, D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R, alpha=0.5,
    #                                            brugg=self.brugg, SOC=self.SOC, T=self.T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
    #     self.assertEqual(self.T, electrode.T)
    #     self.assertEqual(1.0e-14, electrode.D())

    #     electrode.T = temp_new1
    #     self.assertEqual(temp_new1, electrode.T)
    #     self.assertEqual(1.75130006059155e-14, electrode.D())

    #     electrode.T = temp_new2
    #     self.assertEqual(temp_new2, electrode.T)
    #     self.assertAlmostEqual(3.427480746e-15, electrode.D(), places=18)

    # def test_method_get_k(self):
    #     temp_new1: float = 313.15  # [K]
    #     temp_new2: float = 273.15  # [K]
    #     electrode: bc.Electrode = bc.Electrode(L=self.L, A=self.A, kappa=self.kappa, epsilon=self.epsilon, max_conc=self.max_conc, R=self.R, S=self.S,
    #                                            T_ref=self.T_ref, D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R, alpha=0.5,
    #                                            brugg=self.brugg, SOC=self.SOC, T=self.T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
    #     self.assertEqual(self.T, electrode.T)
    #     self.assertEqual(6.67e-11, electrode.k())

    #     electrode.T = temp_new1
    #     self.assertEqual(temp_new1, electrode.T)
    #     self.assertAlmostEqual(2.04586150e-10, electrode.k(), places=13)

    #     electrode.T = temp_new2
    #     self.assertEqual(temp_new2, electrode.T)
    #     self.assertAlmostEqual(7.835665385e-12, electrode.k(), places=13)

    # def test_method_ocp(self) -> None:
    #     """
    #     Tests for the calculated ocp value at the reference temperature
    #     """
    #     electrode: bc.Electrode = bc.Electrode(L=self.L, A=self.A, kappa=self.kappa, epsilon=self.epsilon, max_conc=self.max_conc, R=self.R, S=self.S,
    #                                            T_ref=self.T_ref, D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R, alpha=0.5,
    #                                            brugg=self.brugg, SOC=self.SOC, T=self.T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
    #     self.assertEqual(OCP_ref_p(SOC=self.SOC), electrode.ocp())

    #     # Now change the soc
    #     soc_new: float = 0.5
    #     electrode.soc = soc_new
    #     self.assertEqual(OCP_ref_p(SOC=soc_new), electrode.ocp())

    # def test_method_docpdT(self) -> None:
    #     electrode: bc.Electrode = bc.Electrode(L=self.L, A=self.A, kappa=self.kappa, epsilon=self.epsilon, max_conc=self.max_conc, R=self.R, S=self.S,
    #                                            T_ref=self.T_ref, D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R, alpha=0.5,
    #                                            brugg=self.brugg, SOC=self.SOC, T=self.T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
    #     self.assertEqual(dOCPdT_p(SOC=self.SOC), electrode.docpdT())
