"""
Contains the Python's unittests for the classes pertaining to the battery components.
"""

__all__ = ['TestElectrode', "TestNElectrode", "TestPElectrode", "TestElectrolyte", "TestBatteryCell"]

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by Moin Ahmed. All Rights Reserved."
__status__ =  "deployed"

import unittest

import bmslogic.simulations.cell.cell as bc
from .parameters_funcs import *


class TestElectrode(unittest.TestCase):
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

    electrode: bc.Electrode = bc.Electrode(
        L=L, A=A, kappa=kappa, epsilon=epsilon, max_conc=max_conc, R=R, S=S,
        T_ref=T_ref, D_ref=D_ref, k_ref=k_ref, Ea_D=Ea_D, Ea_R=Ea_R, alpha=0.5,
        brugg=brugg, SOC=SOC, T=T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)

    def test_properties(self) -> None:
        electrode: bc.Electrode = bc.Electrode(L=self.L, A=self.A, kappa=self.kappa, epsilon=self.epsilon, max_conc=self.max_conc, R=self.R, S=self.S,
                                               T_ref=self.T_ref, D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R, alpha=0.5,
                                               brugg=self.brugg, SOC=self.SOC, T=self.T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)

        self.assertAlmostEqual(self.T, electrode.T)
        self.assertAlmostEqual(self.SOC, electrode.soc)
        self.assertAlmostEqual(self.A, electrode.A)
        self.assertAlmostEqual(self.S, electrode.S)
        self.assertAlmostEqual(self.max_conc, electrode.c_max)

    def test_method_get_D(self):
        temp_new1: float = 313.15  # [K]
        temp_new2: float = 273.15  # [K]
        electrode: bc.Electrode = bc.Electrode(L=self.L, A=self.A, kappa=self.kappa, epsilon=self.epsilon, max_conc=self.max_conc, R=self.R, S=self.S,
                                               T_ref=self.T_ref, D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R, alpha=0.5,
                                               brugg=self.brugg, SOC=self.SOC, T=self.T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
        self.assertEqual(self.T, electrode.T)
        self.assertEqual(1.0e-14, electrode.D())

        electrode.T = temp_new1
        self.assertEqual(temp_new1, electrode.T)
        self.assertEqual(1.75130006059155e-14, electrode.D())

        electrode.T = temp_new2
        self.assertEqual(temp_new2, electrode.T)
        self.assertAlmostEqual(3.427480746e-15, electrode.D(), places=18)

    def test_method_get_k(self):
        temp_new1: float = 313.15  # [K]
        temp_new2: float = 273.15  # [K]
        electrode: bc.Electrode = bc.Electrode(L=self.L, A=self.A, kappa=self.kappa, epsilon=self.epsilon, max_conc=self.max_conc, R=self.R, S=self.S,
                                               T_ref=self.T_ref, D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R, alpha=0.5,
                                               brugg=self.brugg, SOC=self.SOC, T=self.T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
        self.assertEqual(self.T, electrode.T)
        self.assertEqual(6.67e-11, electrode.k())

        electrode.T = temp_new1
        self.assertEqual(temp_new1, electrode.T)
        self.assertAlmostEqual(2.04586150e-10, electrode.k(), places=13)

        electrode.T = temp_new2
        self.assertEqual(temp_new2, electrode.T)
        self.assertAlmostEqual(7.835665385e-12, electrode.k(), places=13)

    def test_method_ocp(self) -> None:
        """
        Tests for the calculated ocp value at the reference temperature
        """
        soc_old: float = self.SOC
        electrode: bc.Electrode = bc.Electrode(L=self.L, A=self.A, kappa=self.kappa, epsilon=self.epsilon, max_conc=self.max_conc, R=self.R, S=self.S,
                                               T_ref=self.T_ref, D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R, alpha=0.5,
                                               brugg=self.brugg, SOC=self.SOC, T=self.T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
        self.assertEqual(OCP_ref_p(SOC=self.SOC), electrode.ocp())

        # Now change the soc
        soc_new: float = 0.5
        electrode.soc = soc_new
        self.assertEqual(OCP_ref_p(SOC=soc_new), electrode.ocp())

    def test_method_docpdT(self) -> None:
        electrode: bc.Electrode = bc.Electrode(L=self.L, A=self.A, kappa=self.kappa, epsilon=self.epsilon, max_conc=self.max_conc, R=self.R, S=self.S,
                                               T_ref=self.T_ref, D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R, alpha=0.5,
                                               brugg=self.brugg, SOC=self.SOC, T=self.T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
        self.assertEqual(dOCPdT_p(SOC=self.SOC), electrode.docpdT())


class TestNElectrode(unittest.TestCase):
    T: float = 298.15
    SOC_init: float = 0.59
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
    SOC_init_n: float = 0.59

    n_electrode: bc.NElectrode = bc.NElectrode(L=L_n, A=A_n, kappa=kappa_n, epsilon=epsilon_n, max_conc=max_conc_n, R=R_n, S=S_n, 
                                               T_ref=T_ref_n, D_ref=D_ref_n, k_ref=k_ref_n, Ea_D=Ea_D_n, Ea_R=Ea_R_n, alpha=alpha_n,
                                               brugg=brugg_n, SOC=SOC_init_n, T=T, func_OCP=OCP_ref_n, func_dOCPdT=dOCPdT_n)
    
    def test_properties(self) -> None:
        self.assertAlmostEqual(self.T, self.n_electrode.T)
        self.assertAlmostEqual(self.SOC_init, self.n_electrode.soc)

        # change temp
        new_T: float = 300.15
        self.n_electrode.T = new_T
        self.assertEqual(new_T, self.n_electrode.T)

        # change soc
        new_soc: float = 0.61
        self.n_electrode.soc = new_soc
        self.assertEqual(new_soc, self.n_electrode.soc)

    def test_method_ocp(self) -> None:
        """
        Tests for the calculated ocp value at the reference temperature
        """
        T: float = 298.15
        electrode: bc.NElectrode = bc.NElectrode(L=self.L_n, A=self.A_n, kappa=self.kappa_n, epsilon=self.epsilon_n, max_conc=self.max_conc_n, R=self.R_n, S=self.S_n, 
                                                 T_ref=self.T_ref_n, D_ref=self.D_ref_n, k_ref=self.k_ref_n, Ea_D=self.Ea_D_n, Ea_R=self.Ea_R_n, alpha=self.alpha_n,
                                                 brugg=self.brugg_n, SOC=self.SOC_init, T=T, func_OCP=OCP_ref_n, func_dOCPdT=dOCPdT_n)
        self.assertAlmostEqual(OCP_ref_n(SOC=self.SOC_init), electrode.ocp())

        # Now change the soc
        soc_new: float = 0.5
        electrode.soc = soc_new
        self.assertAlmostEqual(OCP_ref_n(SOC=soc_new), electrode.ocp())


class TestPElectrode(unittest.TestCase):
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
    T: float = 298.15
    SOC_init_p: float = 0.59
    SOC_p: float = SOC_init_p
    soc_min_p: float = 0.4956 
    soc_max_p: float = 0.989011
    alpha_p: float = 0.5

    p_electrode: bc.PElectrode = bc.PElectrode(
        L=L_p, A=A_p, kappa=kappa_p, epsilon=epsilon_p, max_conc=max_conc_p, R=R_p, S=S_p,
        T_ref=T_ref_p, D_ref=D_ref_p, k_ref=k_ref_p, Ea_D=Ea_D_p, Ea_R=Ea_R_p, alpha=alpha_p,
        brugg=brugg_p, SOC=SOC_init_p, T=T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
    
    def test_properties(self):
        self.assertAlmostEqual(self.T, self.p_electrode.T)
        self.assertAlmostEqual(self.SOC_p, self.p_electrode.soc)

        # change temp
        new_T: float = 300.15
        self.p_electrode.T = new_T
        self.assertEqual(new_T, self.p_electrode.T)

        # change soc
        new_soc: float = 0.61
        self.p_electrode.soc = new_soc
        self.assertEqual(new_soc, self.p_electrode.soc)
    
    def test_methods(self):
        electrode: bc.Electrode = bc.Electrode(L=self.L_p, A=self.A_p, kappa=self.kappa_p, epsilon=self.epsilon_p, max_conc=self.max_conc_p, R=self.R_p, S=self.S_p,
                                               T_ref=self.T_ref_p, D_ref=self.D_ref_p, k_ref=self.k_ref_p, Ea_D=self.Ea_D_p, Ea_R=self.Ea_R_p, alpha=0.5,
                                               brugg=self.brugg_p, SOC=self.SOC_p, T=self.T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
        self.assertAlmostEqual(OCP_ref_p(SOC=self.SOC_p), electrode.ocp())

        # Now change the soc
        soc_new: float = 0.5
        electrode.soc = soc_new
        self.assertAlmostEqual(OCP_ref_p(SOC=soc_new), electrode.ocp())


class TestElectrolyte(unittest.TestCase):
    L_e: float = 2e-5
    c_init_e: float = 1000.0
    kappa_e: float = 0.2875
    epsilon_e: float = 0.724
    brugg_e: float = 1.5

    electrolyte: bc.Electrolyte = bc.Electrolyte(L=L_e, conc=c_init_e, kappa=kappa_e, epsilon=epsilon_e, brugg=brugg_e)

    def test_properties(self):
        """
        This test checks if Electrolyte class is able to assign and read the electrolyte parameters correctly.
        """
        self.assertEqual(self.c_init_e, self.electrolyte.conc)
        self.assertEqual(self.L_e, self.electrolyte.L)
        self.assertEqual(self.kappa_e, self.electrolyte.kappa)
        self.assertEqual(self.epsilon_e, self.electrolyte.epsilon)
        self.assertEqual(self.brugg_e, self.electrolyte.brugg)
        self.assertEqual(self.kappa_e * self.epsilon_e ** self.brugg_e, self.electrolyte.kappa_eff())


class TestBatteryCell(unittest.TestCase):
    # PElectrode Parameters
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
    T: float = 298.15
    SOC_init_p: float = 0.59
    SOC_p: float = SOC_init_p
    soc_min_p: float = 0.4956
    soc_max_p: float = 0.989011
    alpha_p: float = 0.5

    # NElectrode parameters
    T: float = 298.15
    SOC_n: float = 0.59
    SOC_init_n: float = SOC_n
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

    # Electrolyte parameters
    L_e: float = 2e-5
    c_init_e: float = 1000.0
    kappa_e: float = 0.2875
    epsilon_e: float = 0.724
    brugg_e: float = 1.5

    # BatteryCell parameters
    rho: float = 1626
    Vol: float = 3.38e-5
    C_p: float = 750
    h: float = 1
    A: float = 0.085
    cap: float = 1.65
    V_max: float = 4.2
    V_min: float = 2.5
    R_cell: float = 0.00282300384424832

    def check_BatteryCell_properties(self, instance_BatteryCell: bc.BatteryCell) -> None:
        """Appies the asserts on relevant attributes and methods of an BatteryCell instance

        Args:
            instance_BatteryCell (sp.BatteryCell): instance of an BatteryCell
        """
        self.assertEqual(self.T, instance_BatteryCell.T())
        self.assertEqual(self.rho, instance_BatteryCell.rho())
        self.assertEqual(self.Vol, instance_BatteryCell.vol())
        self.assertEqual(self.C_p, instance_BatteryCell.C_p())
        self.assertEqual(self.h, instance_BatteryCell.h())
        self.assertEqual(self.A, instance_BatteryCell.A())
        self.assertEqual(self.V_max, instance_BatteryCell.V_max())
        self.assertEqual(self.V_min, instance_BatteryCell.V_min())
        self.assertEqual(self.R_cell, instance_BatteryCell.R_cell)

    def check_BatteryCell_electrolyte_properties(self, instance_BatteryCell: bc.BatteryCell):
        self.assertEqual(self.L_e, instance_BatteryCell.electrolyte.L)
        self.assertEqual(self.c_init_e, instance_BatteryCell.electrolyte.conc)
        self.assertEqual(self.kappa_e, instance_BatteryCell.electrolyte.kappa)
        self.assertEqual(self.epsilon_e, instance_BatteryCell.electrolyte.epsilon)
        self.assertAlmostEqual(self.brugg_e, instance_BatteryCell.electrolyte.brugg)

    def test_constructor1(self) -> None:
        """ This method checks for the BatteryCell's attribute and methods when the BatteryCell class is initialiated with one of the constructors.

        """
        p_electrode: bc.PElectrode = bc.PElectrode(L=self.L_p, A=self.A_p, kappa=self.kappa_p, epsilon=self.epsilon_p, max_conc=self.max_conc_p,
                                                   R=self.R_p, S=self.S_p, T_ref=self.T_ref_p, D_ref=self.D_ref_p, k_ref=self.k_ref_p,
                                                   Ea_D=self.Ea_D_p, Ea_R=self.Ea_R_p, alpha=self.alpha_p,
                                                   brugg=self.brugg_p, SOC=self.SOC_init_p, T=self.T,
                                                   func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
        n_electrode: bc.NElectrode = bc.NElectrode(L=self.L_n, A=self.A_n, kappa=self.kappa_n, epsilon=self.epsilon_n, max_conc=self.max_conc_n,
                                                   R=self.R_n, S=self.S_n, T_ref=self.T_ref_n, D_ref=self.D_ref_n, k_ref=self.k_ref_n,
                                                   Ea_D=self.Ea_D_n, Ea_R=self.Ea_R_n, alpha=self.alpha_n,
                                                   brugg=self.brugg_n, SOC=self.SOC_init_n, T=self.T,
                                                   func_OCP=OCP_ref_n, func_dOCPdT=dOCPdT_n)
        electrolyte: bc.Electrolyte = bc.Electrolyte(
            L=self.L_e, conc=self.c_init_e, kappa=self.kappa_e, epsilon=self.epsilon_e, brugg=self.brugg_e)
        battery_cell: bc.BatteryCell = bc.BatteryCell(p_elec=p_electrode, n_elec=n_electrode, electrolyte=electrolyte,
                                                      rho=self.rho, Vol=self.Vol, C_p=self.C_p, h=self.h, A=self.A, cap=self.cap,
                                                      V_max=self.V_max, V_min=self.V_min, R_cell=self.R_cell)
        self.check_BatteryCell_properties(instance_BatteryCell=battery_cell)

    def test_constructor2(self) -> None:
        """This method checks for the BatteryCell's attribute and methods when the BatteryCell class is initialiated with one of the constructors.
        """
        battery_cell: bc.BatteryCell = bc.BatteryCell(L_p=self.L_p, A_p=self.A_p, kappa_p=self.kappa_p, epsilon_p=self.epsilon_p, max_conc_p=self.max_conc_p,
                                                      R_p=self.R_p, S_p=self.S_p, T_ref_p=self.T_ref_p, D_ref_p=self.D_ref_p, k_ref_p=self.k_ref_p,
                                                      Ea_D_p=self.Ea_D_p, Ea_R_p=self.Ea_R_p, alpha_p=self.alpha_p,
                                                      brugg_p=self.brugg_p, SOC_p=self.SOC_init_p, T_p=self.T,
                                                      func_OCP_p=OCP_ref_p, func_dOCPdT_p=dOCPdT_p,

                                                      conc_e=self.c_init_e, L_s=self.L_e, kappa_s=self.kappa_e, epsilon_s=self.epsilon_e, brugg_s=self.brugg_e,

                                                      L_n=self.L_n, A_n=self.A_n, kappa_n=self.kappa_n, epsilon_n=self.epsilon_n, max_conc_n=self.max_conc_n,
                                                      R_n=self.R_n, S_n=self.S_n, T_ref_n=self.T_ref_n, D_ref_n=self.D_ref_n, k_ref_n=self.k_ref_n,
                                                      Ea_D_n=self.Ea_D_n, Ea_R_n=self.Ea_R_n, alpha_n=self.alpha_n,
                                                      brugg_n=self.brugg_n, SOC_n=self.SOC_init_n, T_n=self.T,
                                                      func_OCP_n=OCP_ref_n, func_dOCPdT_n=dOCPdT_n,

                                                      rho=self.rho, Vol=self.Vol, C_p=self.C_p, h=self.h, A=self.A, cap=self.cap, 
                                                      V_max=self.V_max, V_min=self.V_min, R_cell=self.R_cell)
        self.check_BatteryCell_properties(instance_BatteryCell=battery_cell)
        self.check_BatteryCell_electrolyte_properties(instance_BatteryCell=battery_cell)

    def test_properties(self):
        pass
