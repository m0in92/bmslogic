from random import randint
import sys
import unittest

import numpy
import numpy as np

from bmslogic.simulations.applications.external_conditions import ExternalConditions
from bmslogic.simulations.applications.drivecycles import EVDriveCycle
from bmslogic.simulations.applications.ev import EV, EVFromDatabase, EVDynamics


class TestEVConstructor(unittest.TestCase):
    def test_EV_attributes(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        # Check for vehicle basic information
        self.assertEqual(alias_name, volt.alias_name)
        self.assertEqual("Volt", volt.model_name)
        self.assertEqual("2017", volt.year)
        self.assertEqual("Chevy", volt.manufacturer)
        # Check for battery pack information
        self.assertEqual("Unknown", volt.pack.cell_manufacturer)
        self.assertEqual("Unknown", volt.pack.cell_chem)
        self.assertEqual(15.0, volt.pack.cell_cap)
        self.assertEqual(450.0, volt.pack.cell_mass)
        self.assertEqual(4.2, volt.pack.cell_V_max)
        self.assertEqual(3.8, volt.pack.cell_V_nom)
        self.assertEqual(3, volt.pack.cell_V_min)
        self.assertEqual(3, volt.pack.Np)
        self.assertEqual(8, volt.pack.Ns)
        self.assertEqual(0.08, volt.pack.module_overhead_mass)
        self.assertEqual(12, volt.pack.num_modules)
        self.assertEqual(0.1, volt.pack.pack_overhead_mass)
        self.assertEqual(75, volt.pack.SOC_full)
        self.assertEqual(25, volt.pack.SOC_empty)
        self.assertEqual(0.96, volt.pack.eff)
        # Check for other vehicle information
        self.assertEqual(0.0111, volt.C_r)
        self.assertEqual(0.22, volt.C_d)
        self.assertEqual(1425.0, volt.m)
        self.assertEqual(75.0, volt.payload_capacity)
        self.assertEqual(200.0, volt.overhead_power)

    def test_motor_attributes(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        # Check for vehicle drivetrain information
        self.assertEqual(0.35, volt.drive_train.wheel.r)
        self.assertEqual(8.0, volt.drive_train.wheel.I)
        self.assertEqual(4, volt.drive_train.num_wheel)
        self.assertEqual(0.94, volt.drive_train.inverter_eff)
        self.assertEqual(0.9, volt.drive_train.frac_regen_torque)
        self.assertEqual(0.8316, volt.drive_train.eff)


    def test_property_attributes(self):
        """
        Tests the EV property attributes. The expected numbers have been attained from Plett's MATLAB code.
        :return:
        """
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        self.assertAlmostEqual(1.581521739130435e+03, volt.curb_mass)
        self.assertAlmostEqual(1.656521739130435e+03, volt.max_mass)
        self.assertEqual(5.551020408163266e+02, volt.rot_mass)
        self.assertAlmostEqual(2.211623779946761e+03, volt.equiv_mass)
        self.assertAlmostEqual(1.319468914507713e+02, volt.max_speed)

    def test_motor_attributes(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        self.assertEqual(275, volt.motor.L_max)
        self.assertEqual(4000, volt.motor.RPM_r)
        self.assertEqual(12000, volt.motor.RPM_max)
        self.assertEqual(0.95, volt.motor.eff)
        self.assertEqual(0.2, volt.motor.I)
        self.assertAlmostEqual(1.151917306316258e+02, volt.motor.P_max)

class TestEVReprAndStr(unittest.TestCase):
    alias_name = "Volt_2017"
    volt = EVFromDatabase(alias_name=alias_name)
    def test_repr(self):
        # alias_name = "Volt_2017"
        # volt = EVFromDatabase(alias_name=alias_name)
        repr(self.volt)
        self.assertEqual(f"EV('{self.alias_name}')", repr(self.volt))

    def test_str(self):
        # alias_name = "Volt_2017"
        # volt = EVFromDatabase(alias_name=alias_name)
        self.assertEqual(f"{self.alias_name} made by Chevy", str(self.volt))


np.set_printoptions(threshold=sys.maxsize)

class TestVehicleDynamics(unittest.TestCase):
    drive_cycle_name = "udds"
    def test_des_speed(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        self.assertEqual(1.341120000000000, model.des_speed[21])
        self.assertEqual(14.484096000000000, model.des_speed[113])
        self.assertAlmostEqual(0.983488000000000, model.des_speed[124])

    def test_sim_desired_acceleration(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the desired accelerations.
        self.assertEqual(1.341120000000000, sol.des_acc[21])
        self.assertAlmostEqual(1.296416000000000, sol.des_acc[22])
        self.assertAlmostEqual(-0.938784000000000, sol.des_acc[39])
        self.assertEqual(-1.475232000000000, sol.des_acc[119])
        self.assertAlmostEqual(1.430527999999997, sol.des_acc[194])

    def test_sim_acceleration_force(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the desired acceleration force.
        self.assertAlmostEqual(2.966052883762201e+03, sol.des_acc_F[21])
        self.assertEqual(7.909474356699195e+02, sol.des_acc_F[28])
        self.assertEqual(-3.262658172138421e+03, sol.des_acc_F[119])

    def test_sim_aero_force(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the desired areodynamic drag.
        self.assertAlmostEqual(0.445945591719936, sol.aero_F[22])
        self.assertEqual(23.981962932494340, sol.aero_F[119])

    def test_roll_grade_force(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the desired roll grade force.
        self.assertEqual(48.751215402632994, sol.roll_grade_F[20])
        self.assertAlmostEqual(2.291315240982852e+02, sol.roll_grade_F[119])

    def test_sim_demand_torque(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the demand torque.
        self.assertAlmostEqual(1.421910449243462, sol.demand_torque[0])
        self.assertEqual(-87.778386648972870, sol.demand_torque[119])

    def test_sim_max_torque(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the max. torque
        self.assertEqual(275, sol.max_torque[0])
        self.assertEqual(2.732933241759195e+02, sol.max_torque[84])
        self.assertEqual(275.0, sol.max_torque[119])

    def test_sim_limit_regeneration(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the limit regeneration
        self.assertEqual(2.475000000000000e+02, sol.limit_regen[0])
        self.assertEqual(2.363385665043329e+02, sol.limit_regen[112])
        self.assertEqual(2.475000000000000e+02, sol.limit_regen[119])

    def test_sim_limit_torque(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the limit torque
        self.assertAlmostEqual(1.421910449243462, sol.limit_torque[0])
        self.assertAlmostEqual(-87.778386648972870, sol.limit_torque[119])

    def test_sim_motor_torque(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the motor torque
        self.assertAlmostEqual(1.421910449243462, sol.motor_torque[0])
        self.assertEqual(87.931786225640980, sol.motor_torque[21])
        self.assertEqual(-87.778386648972870, sol.motor_torque[119])

    def test_sim_actual_acceleration_force(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the actual acceleration force
        self.assertEqual(0.0, sol.actual_acc_F[0])
        self.assertEqual(2.966052883762201e+03, sol.actual_acc_F[21])
        self.assertAlmostEqual(-3.262658172138421e+03, sol.actual_acc_F[119])

    def test_sim_actual_acceleration(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the actual acceleration
        self.assertEqual(0.0, sol.actual_acc[0])
        self.assertAlmostEqual(1.341120000000000, sol.actual_acc[21])
        self.assertAlmostEqual(-1.475232000000000, sol.actual_acc[119])

    def test_sim_motor_speed(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the motor speed
        self.assertEqual(0.0, sol.motor_speed[0])
        self.assertEqual(4.390886618319142e+02, sol.motor_speed[21])
        self.assertEqual(2.736985992085598e+03, sol.motor_speed[119])

    def test_sim_actual_speed(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the actual speed
        self.assertEqual(0.0, sol.actual_speed[0])
        self.assertEqual(1.341120000000000, sol.actual_speed[21])
        self.assertEqual(8.359648000000000, sol.actual_speed[119])

    def test_sim_demand_power(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the demand power
        self.assertEqual(0.0, sol.demand_power[0])
        self.assertEqual(2.021607036735971, sol.demand_power[21])
        self.assertEqual(-27.378622520221082, sol.demand_power[119])

    def test_sim_limit_power(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the limit power
        self.assertEqual(0.0, sol.limit_power[0])
        self.assertEqual(2.021607036735971, sol.limit_power[21])
        self.assertEqual(-27.378622520221082, sol.limit_power[119])

    def test_battery_demand(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the battery demand
        self.assertEqual(0.2, sol.battery_demand[0])
        # self.assertEqual(2.631097151114207, sol.battery_demand[21])
        self.assertAlmostEqual(-22.567011148711070, sol.battery_demand[119], places=2)

    def test_sim_cell_current(self):
        alias_name = "Volt_2017"
        volt = EVFromDatabase(alias_name=alias_name)
        np_test = randint(1,100)
        volt.pack.Np = np_test # assign Np to a randomly generated int value
        udds = EVDriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        model = EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for cell current
        self.assertIs(type(sol.current), type(numpy.empty(0)))
        self.assertIs(type(sol.cell_current), type(numpy.empty(0)))
        self.assertEqual(len(sol.current), len(sol.cell_current))
        for indx in range(len(sol.current)):
            quotient = sol.current[indx] / sol.cell_current[indx]
            self.assertAlmostEqual(quotient, np_test, None, "Current ratio does not match the assigned ", 0.000001)

