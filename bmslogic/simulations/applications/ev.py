"""
This module provides the classes pertaining to the parameters and functionailities of the various components of an
electric vehicle.
"""

__all__ = ['ACInductionMotor', 'Wheel', 'Gearbox', 'DriveTrain', 'BatteryCell', 'BatteryModule', 'BatteryPack', 'EV',
           'EVFromDatabase', "EVDynamics"]

__authors__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All rights reserved."
__status__ = "Deployed"


from collections.abc import Callable
import os
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd

from bmslogic import path_definations
from bmslogic.calc_helpers.constants import Constants
from bmslogic.calc_helpers.utils import timer

from bmslogic.simulations.applications.external_conditions import ExternalConditions
from bmslogic.simulations.applications.drivecycles import EVDriveCycle
from bmslogic.simulations.applications.sol import Solution


@dataclass
class ACInductionMotor:
    motor_type: float  # motor type
    RPM_r: float  # rated motor speed, rpm
    RPM_max: float  # max. motor speed, rpm
    L_max: float  # max. torque, Nm
    eff: float  # motor efficiency, unit-less
    I: float  # motor inertia, kg/m2

    def __post_init__(self):
        # check for the input motor type. np.isnan is possible in case of empty field in the EV_dataset.csv
        if isinstance(self.motor_type, str) or np.isnan(self.motor_type):
            if isinstance(self.motor_type, str):
                self.motor_type = self.motor_type
            else:
                self.motor_type = "Unknown"  # set instance's motor type in case it is missing
        else:
            raise TypeError(
                "Motor type needs to be a string or np.nan (in case it is unknown) type.")

        if not isinstance(self.RPM_r, float):
            raise TypeError("Rated motor speed needs to be a float.")

        if not isinstance(self.RPM_max, float):
            raise TypeError("Max. motor speed needs to be a float.")

        if not isinstance(self.L_max, float):
            raise TypeError("Max. motor torque needs to be a float.")

        if not isinstance(self.eff, float):
            raise TypeError("Motor efficiency needs to be a float.")

        if not isinstance(self.I, float):
            raise TypeError("Motor efficiency needs to be a float.")

        self.P_max = 2 * np.pi * self.L_max * self.RPM_r / 60000  # max motor power, kW


@dataclass
class Wheel:
    r: float  # wheel radius
    I: float  # wheel inertia

    def __post_init__(self):
        if not isinstance(self.r, float):
            raise TypeError("Wheel radius needs to be a float.")
        if not isinstance(self.I, float):
            raise TypeError("Wheel inertia needs to be a float.")


@dataclass()
class Gearbox:
    N: float  # gear box ratio
    I: float  # gearbox inertia

    def __post_init__(self):
        if not isinstance(self.N, float):
            raise TypeError("Gearbox ratio needs to be a float.")
        if not isinstance(self.I, float):
            raise TypeError("Gearbox inertia needs to be a float.")


@dataclass
class DriveTrain:
    wheel_radius: int  # wheel radius, m
    wheel_inertia: float  # wheel inertia, kg/m2
    num_wheel: int  # number of wheels in a drivetrain
    gearbox_ratio: float  # gearbox ratio
    gearbox_inertia: float  # gearbox inertia, kg/m2
    inverter_eff: float  # inverter efficiency, unit-less
    frac_regen_torque: float  # fraction of regenerated torque
    eff: float  # drivetrain efficiency

    def __post_init__(self):
        self.wheel = Wheel(r=self.wheel_radius,
                           I=self.wheel_inertia)  # Wheel object
        del self.wheel_radius, self.wheel_inertia

        if not isinstance(self.num_wheel, int):
            raise TypeError("Number of wheels needs to an integer.")

        self.gear_box = Gearbox(N=self.gearbox_ratio,
                                I=self.gearbox_inertia)  # Gearbox object
        del self.gearbox_ratio, self.gearbox_inertia

        if not isinstance(self.inverter_eff, float):
            raise TypeError("Inverter efficiency needs to be a float.")

        if not isinstance(self.frac_regen_torque, float):
            raise TypeError("Frac_regen_torque needs to be a float.")

        if not isinstance(self.eff, float):
            raise TypeError("Drivetrain efficiency needs to be a float.")


@dataclass
class BatteryCell:
    cell_manufacturer: str  # Battery cell manufacturer
    cell_cap: float  # Battery cell capacity, A hr
    cell_mass: float  # Battery cell mass, g
    cell_V_max: float  # Battery cell max. voltage, V
    cell_V_nom: float  # Battery cell nominal voltage, V
    cell_V_min: float  # Battery cell min. voltage, V
    cell_chem: str  # Battery positive electrode chemistry

    def __post_init__(self):
        # check for the input manufacturer type. np.isnan is possible in case of empty field in the EV_dataset.csv
        if isinstance(self.cell_manufacturer, str) or pd.isnull(self.cell_manufacturer):
            if isinstance(self.cell_manufacturer, str):
                self.cell_manufacturer = self.cell_manufacturer
            else:
                # sets the instance value in case of unknown values.
                self.cell_manufacturer = "Unknown"
        else:
            raise TypeError(
                "Battery cell manufacturer needs to be a string or np.nan type.")

        if not isinstance(self.cell_cap, float):
            raise TypeError('cell_cap needs to be a float type.')
        if not isinstance(self.cell_mass, float):
            raise TypeError('cell_mass needs to be a float type.')
        if not isinstance(self.cell_V_max, float):
            raise TypeError('cell_V_max needs to be a float type.')
        if not isinstance(self.cell_V_nom, float):
            raise TypeError('cell_V_nom needs to be a float type.')
        if not isinstance(self.cell_V_min, float):
            raise TypeError('cell_V_min needs to be a float type.')

        if isinstance(self.cell_chem, str) or np.isnan(self.cell_chem):
            if isinstance(self.cell_chem, str):
                self.cell_chem = self.cell_chem  # Battery cell postive electrode chemistry
            else:
                self.cell_chem = "Unknown"
        else:
            raise TypeError(
                "Cell chemistry needs to be a string or a np.nan type.")

        self.cell_energy = self.cell_V_nom * self.cell_cap  # Battery cell energy, W hr
        self.cell_spec_energy = 1000 * self.cell_energy / \
            self.cell_mass  # Battery cell specific energy, W hr/kg


@dataclass
class BatteryModule(BatteryCell):
    Ns: int
    Np: int
    module_overhead_mass: float

    def __post_init__(self):
        super().__post_init__()

        self.total_no_cells = self.Ns * self.Np
        self.module_cap = self.Np * self.cell_cap  # Battery module capacity,  A hr
        self.module_mass = self.total_no_cells * \
            (self.cell_mass / 1000) / \
            (1 - self.module_overhead_mass)  # Battery module mass, kg
        self.module_energy = self.total_no_cells * \
            self.cell_energy / 1000  # Battery module energy, kWh
        self.module_specific_energy = self.module_energy * \
            1000 / self.module_mass  # Specific energy, Wh/kg


@dataclass
class BatteryPack(BatteryModule):
    num_modules: int  # no. of modules in series, unit-less
    pack_overhead_mass: float  # mass beyond module and cell masses, percent
    SOC_full: float  # Battery pack state-of-charge when full, percent
    SOC_empty: float  # Battery pack state-of-charge when empty, percent
    eff: float  # battery pack efficiency

    def __post_init__(self):
        super().__post_init__()

        # total no. of battery cells in the pack, unit-less
        self.total_no_cells = self.total_no_cells * self.num_modules
        self.pack_mass = self.module_mass * self.num_modules / \
            (1 - self.pack_overhead_mass)  # Battery pack mass, kg
        self.pack_energy = self.module_energy * \
            self.num_modules  # Battery pack energy, Wh
        self.pack_specific_energy = self.pack_energy * 1000 / \
            self.pack_mass  # Battery pack specific energy, Wh/kg
        self.pack_V_max = self.num_modules * self.Ns * \
            self.cell_V_max  # Battery pack max. voltage, V
        self.pack_V_nom = self.num_modules * self.Ns * \
            self.cell_V_nom  # Battery pack nominal voltage, V
        self.pack_V_min = self.num_modules * self.Ns * \
            self.cell_V_min  # battery pack min. voltage, V


@dataclass
class EV:
    """
    EV stores all relevant vehicle parameters (e.g., wheel, drivetrain, battery pack, etc.,) as its class attributes.
    Furthermore, its has various vehicle methods to calculate for additional vehicle parameters.
    """
    # Basic EV information
    alias_name: Optional[str] = None
    model_name: Optional[str] = None
    year: Optional[int] = None
    manufacturer: Optional[str] = None
    trim: Optional[str] = None

    # vehicle's component class objects
    drive_train: Optional[DriveTrain] = None
    motor: Optional[ACInductionMotor] = None
    pack: Optional[BatteryPack] = None

    # Other vehicle information
    C_d: Optional[float] = None  # drag coefficient, unit-less
    A_front: Optional[float] = None  # vehicle frontal area, m^2
    m: Optional[float] = None  # vehicle mass, kg
    payload_capacity: Optional[float] = None  # vehicle payload capacity, kg
    overhead_power: Optional[float] = None  # vehicle overhear power, W

    @property
    def curb_mass(self) -> float:
        """
        Vehicle curb mass in units of kg.
        :return: (float) vehicle curb mass, kg
        """
        return self.m + self.pack.pack_mass

    @property
    def max_mass(self) -> float:
        """
        Vehicle maximum mass in units of kg.
        :return: (float) vehicle maximum mass, kg
        """
        return self.curb_mass + self.payload_capacity

    @property
    def rot_mass(self) -> float:
        """
        Vehicle rotating equivalent mass in units of kg.
        :return: (float)
        """
        return ((self.motor.I + self.drive_train.gear_box.I) * (self.drive_train.gear_box.N ** 2) +
                (self.drive_train.wheel.I * self.drive_train.num_wheel))/(self.drive_train.wheel.r ** 2)

    @property
    def equiv_mass(self) -> float:
        """
        Vehicle's equivalent mass is a sum of its maximum and translational equivalent mass of the rotating inertia.
        :return: (float) Vehicle equivalent mass, kg
        """
        return self.max_mass + self.rot_mass

    @property
    def max_speed(self) -> float:
        """
        Vehicle maximum speed in km/h
        :return: (float) Vehicle max. speed, km/h
        """
        return 2 * np.pi * self.drive_train.wheel.r * self.motor.RPM_max * 60 / (1000 * self.drive_train.gear_box.N)


class EVFromDatabase(EV):
    """
    EVFromDatabase inherits from the EV class. It is meant to update the attributes of its parent EV class using the
    Database.
    """

    def __init__(self, alias_name: str, database_dir: str = path_definations.EV_DATABASE_FILE):
        """
        EV class constructor.
        :param alias_name: (str) Vehicle alias [i.e, identifier]
        :param database_dir: (str) The file location of the data/EV/EV_dataset.csv relative to the working directory.
        """
        self.alias_name = alias_name
        df_basicinfo = self.parse_basic_data(file_dir=database_dir)
        model_name = df_basicinfo["model_name"]
        year = df_basicinfo["year"]
        manufacturer = df_basicinfo["manufacturer"]
        trim = df_basicinfo["trim"]
        del df_basicinfo

        df_wheel = self.parse_wheel_info(file_dir=database_dir)
        wheel_radius = float(df_wheel["radius [m]"])
        wheel_inertia = float(df_wheel["inertia [kg/m2]"])
        # rolling coefficient, unit-less
        self.C_r = float(df_wheel["roll_coeff"])
        del df_wheel

        df_drivetrain = self.parse_drivetrain_info(file_dir=database_dir)
        # motor rpm / wheel rpm, unit-less
        gearbox_ratio = float(df_drivetrain["gear_ratio"])
        gearbox_inertia = float(df_drivetrain["gear_inertia [kg/m2]"])
        inverter_eff = float(df_drivetrain["inverter_eff"])
        frac_regen_torque = float(df_drivetrain["frac_regen_torque"])
        dt_eff = float(df_drivetrain["eff"])
        num_wheels = int(df_drivetrain["no_wheels"])
        del df_drivetrain

        drive_train_obj = DriveTrain(wheel_radius=wheel_radius, wheel_inertia=wheel_inertia, num_wheel=num_wheels,
                                     gearbox_ratio=gearbox_ratio, gearbox_inertia=gearbox_inertia,
                                     inverter_eff=inverter_eff, frac_regen_torque=frac_regen_torque, eff=dt_eff)

        df_motor = self.parse_motor_info(file_dir=database_dir)
        motor_type = df_motor["type"]
        rpm_r = float(df_motor["RPM_rated [rpm]"])
        rpm_max = float(df_motor["RPM_max [rpm]"])
        l_max = float(df_motor["Lmax [Nm]"])
        motor_eff = float(df_motor["eff"])
        i_motor = float(df_motor["inertia [kg/m2]"])
        del df_motor
        motor_obj = ACInductionMotor(motor_type=motor_type, RPM_r=rpm_r, RPM_max=rpm_max, L_max=l_max, eff=motor_eff,
                                     I=i_motor)

        df_vehicle = self.parse_veh_info(file_dir=database_dir)
        C_d = float(df_vehicle["C_d"])  # drag coefficient, unit-less
        # vehicle frontal area, m^2
        A_front = float(df_vehicle["frontal_area [m2]"])
        m = float(df_vehicle["mass [kg]"])  # vehicle mass, kg
        # vehicle payload capacity, kg
        payload_capacity = float(df_vehicle["payload_cap [kg]"])
        # vehicle overhear power, W
        overhead_power = float(df_vehicle["overhead_power [W]"])
        del df_vehicle

        df_cell = self.parse_cell_info(file_dir=database_dir)
        cell_manufacturer = df_cell["battery_cell_manufacturer"]
        cell_cap = float(df_cell["capacity [A hr]"])
        cell_mass = float(df_cell["mass [g]"])
        cell_v_max = float(df_cell["V_max [V]"])
        cell_v_nom = float(df_cell["V_nom [V]"])
        cell_v_min = float(df_cell["V_min [V]"])
        cell_chem = df_cell['positive electrode chem.']
        del df_cell
        df_module = self.parse_module_info(file_dir=database_dir)
        n_s = int(df_module["Ns"])
        n_p = int(df_module["Np"])
        module_overhead_mass = float(df_module["overhead_mass [%]"])
        del df_module
        df_pack = self.parse_pack_info(file_dir=database_dir)
        num_modules = int(df_pack["N_module_s"])
        pack_overhead_mass = float(df_pack["overhead_mass [%]"])
        soc_full = float(df_pack["SOC_full"])
        soc_empty = float(df_pack["SOC_empty"])
        pack_eff = float(df_pack["eff"])
        del df_pack
        pack_obj = BatteryPack(cell_manufacturer=cell_manufacturer, cell_cap=cell_cap, cell_mass=cell_mass,
                               cell_V_max=cell_v_max, cell_V_nom=cell_v_nom, cell_V_min=cell_v_min, cell_chem=cell_chem,
                               Ns=n_s, Np=n_p, module_overhead_mass=module_overhead_mass,
                               num_modules=num_modules, pack_overhead_mass=pack_overhead_mass, SOC_full=soc_full,
                               SOC_empty=soc_empty, eff=pack_eff)

        super().__init__(alias_name=alias_name, model_name=model_name, year=year, manufacturer=manufacturer, trim=trim,
                         drive_train=drive_train_obj, motor=motor_obj, pack=pack_obj,
                         C_d=C_d, A_front=A_front, m=m, payload_capacity=payload_capacity, overhead_power=overhead_power)

    @staticmethod
    def list_all_EV_alias(file_dir: str) -> list:
        """
        Lists all the EV alias in the EV database.
        :return: (list) list of all EV alias in the EV database
        """
        df = pd.read_csv(file_dir)
        df.set_index(['Parameter Classification',
                     'Parameter Name'], inplace=True)
        return df.columns.tolist()

    def create_df(self, file_dir: str):
        """
        returns a dataframe containing all the relevant EV information.
        :param file_dir:
        :return:
        """
        df = pd.read_csv(file_dir, header=0)
        df.set_index(['Parameter Classification',
                     'Parameter Name'], inplace=True)
        if self.alias_name not in df.columns:
            raise Exception(f"{self.alias_name} not in EV dataset")
        return df[self.alias_name]

    def parse_basic_data(self, file_dir: str):
        """
        Returns a dataframe containing the basic EV information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["basic vehicle"]

    def parse_wheel_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's motor information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["wheel"]

    def parse_drivetrain_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's drive train information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["drive train"]

    def parse_motor_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's drive train information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["motor"]

    def parse_veh_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's drive train information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["vehicle"]

    def parse_cell_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's battery cell information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["cell"]

    def parse_module_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's battery module information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["module"]

    def parse_pack_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's battery pack information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["pack"]

    def __repr__(self):
        return f"EV('{self.alias_name}')"

    def __str__(self):
        return f"{self.alias_name} made by {self.manufacturer}"


class EVDynamics:
    """
    EVDynamics simulates the demanded power and current from the batter pack.
    """

    def __init__(self, ev_obj: EV, drive_cycle_obj: EVDriveCycle, external_condition_obj: ExternalConditions) -> None:
        """
        EVDynamics class constructor.
        :param ev_obj: (EV) EV class object that contains vehicle parameters.
        :param drive_cycle_obj: (DriveCycle) Drive cycle class object that contains all relevant drive cycle parameters.
        :param external_condition_obj: (ExternalConditions) ExternalConditions class object that contains all relevant
        external condition parameters.
        """
        if isinstance(ev_obj, EV):
            self.EV = ev_obj
        else:
            raise TypeError("ev_obj needs to be a EV object.")

        if isinstance(drive_cycle_obj, EVDriveCycle):
            self.DriveCycle = drive_cycle_obj
        else:
            raise TypeError("DriveCycle_obj needs to be DriveCycle object.")

        if isinstance(external_condition_obj, ExternalConditions):
            self.ExtCond = external_condition_obj
        else:
            raise TypeError(
                "external_condition_onj needs to be External condition object.")

        if isinstance(self.ExtCond.road_grade_angle, np.ndarray):
            if len(self.ExtCond.road_grade_angle) != len(self.DriveCycle.t):
                raise ValueError("The lengths of external condition's road grade and drive cycle's time array do not "
                                 "match.")

    @property
    def des_speed(self) -> np.ndarray:
        """
        Desired vehicle speed in m/s.
        :return: (np.ndarray) Array of desired speed, m/s
        """
        return np.minimum(self.DriveCycle.speed_kmph, self.EV.max_speed) / 3.6

    @staticmethod
    def desired_acc(desired_speed: float, prev_speed: float, current_time: float, prev_time: float) -> float:
        """
        Calculates and returns the desired acceleration, m/s^2.
        :param desired_speed: (float) desired speed, m/s
        :param prev_speed: (float) speed at the previous time step, m/s
        :param current_time: (float): time at the current time step, s
        :param prev_time: (float): time at the previous time step, s
        :return: (float) desired acceleration, m/s^2
        """
        return (desired_speed - prev_speed) / (current_time - prev_time)

    @staticmethod
    def desired_acc_F(equivalent_mass: float, desired_acc: float) -> float:
        """
        Calculates the desired accelerating force in N.
        :param equivalent_mass: (float) Equivalent vehicle mass, kg
        :param desired_acc: (float) acceleration, m/s^2
        :return: (float) desired acceleration
        """
        return equivalent_mass * desired_acc

    @staticmethod
    def aero_F(air_density: float, aero_frontal_area: float, C_d: float, prev_speed: float) -> float:
        """
        Calculates the aerodynamic drag in N.
        :param air_density: External air density, kg/m^3
        :param aero_frontal_area: Vehicle frontal area, m^2
        :param C_d: Drag coefficient, unit-;ess
        :param prev_speed: Speed at the previous time step, m/s
        :return: (float) aerodynamic drag, N
        """
        return 0.5 * air_density * aero_frontal_area * C_d * (prev_speed ** 2)

    @staticmethod
    def roll_grade_F(max_veh_mass: float, gravity_acc: float, grade_angle: float) -> float:
        """
        Calculates the rolling grade force.
        :param C_r: rolling coefficient, unit-less
        :param max_veh_mass: max. vehicle mass, kg
        :param gravity_acc: acceleration of gravity, 9.81 g/m^2
        :param grade_angle: grade_angle, rad
        :return:  (float) rolling grade force, N
        """
        return max_veh_mass * gravity_acc * np.sin(grade_angle)

    @staticmethod
    def demand_torque(des_acc_F: float, aero_F: float, roll_grade_F: float, road_F: float, wheel_radius: float,
                      gear_ratio: float) -> float:
        return (des_acc_F + aero_F + roll_grade_F + road_F) * wheel_radius / gear_ratio

    def init_cond(self):
        """
        Simulation initial conditions
        :return: (float) Returns the initial conditions of the relevant simulation variables.
        """
        prev_speed = 0
        prev_motor_speed = 0
        prev_distance = 0
        prev_SOC = 0
        prev_time = 2 * self.DriveCycle.t[0] - self.DriveCycle.t[1]
        return prev_speed, prev_motor_speed, prev_distance, prev_SOC, prev_time

    def create_init_arrays(self) -> Solution:
        """
        Create numpy arrays with zero elements of the desired sizes for all the simulation results. These simulation
        results are stored in the instance 'sol' of the Solution class.
        :return: (tuple) Solution object whose attributes are numpy arrays with zero elements (except for it's t (time)
        attribute).
        """
        sol = Solution(veh_alias=self.EV.alias_name, t=self.DriveCycle.t)
        return sol

    # @staticmethod
    def simulate_over_all_timesteps(func) -> Callable[[], Solution]:
        """
        Acts as a decorator function, whose wrapper function defines the initial conditions and performs simulation
        iterations over all time steps.
        :param func: (function type) simulation function
        """

        @timer
        def initialize_and_iterations(self) -> Solution:
            # initialization
            prev_speed, prev_motor_speed, prev_distance, prev_SOC, prev_time = self.init_cond()
            sol = self.create_init_arrays()  # create arrays for results and calculations
            # Run the simulation.
            for k in range(len(self.DriveCycle.t)):  # k represents time index.
                func(self, sol, k, prev_time, prev_speed,
                     prev_motor_speed, prev_distance, prev_SOC)
                # update relevant variables below
                prev_time = self.DriveCycle.t[k]
                prev_speed = sol.actual_speed[k]
                prev_motor_speed = sol.motor_speed[k]
                prev_distance = sol.distance[k]
                prev_SOC = sol.battery_SOC[k]
            return sol

        return initialize_and_iterations

    @simulate_over_all_timesteps
    def simulate(self, sol: Solution, k: int, prev_time: float, prev_speed: float, prev_motor_speed: float,
                 prev_distance: float, prev_SOC: float) -> None:
        """
        Performs vehicle dynamics simulation at a specific time step, k. It updates the Solution instance attributes
        at this time step, k.
        :param sol: Solution object that contains the all the simulation results in a arrays.
        :param k: time step
        :param prev_time: time at the previous time step
        :param prev_speed: speed at the previous time step
        :param prev_motor_speed: motor speed at the previous time step.
        :param prev_distance: distance at the previous time step.
        :param prev_SOC: SOC at the previous time step.
        :return: (None)
        """
        sol.des_acc[k] = EVDynamics.desired_acc(desired_speed=self.des_speed[k], prev_speed=prev_speed,
                                                current_time=self.DriveCycle.t[k], prev_time=prev_time)
        sol.des_acc_F[k] = EVDynamics.desired_acc_F(
            equivalent_mass=self.EV.equiv_mass, desired_acc=sol.des_acc[k])
        sol.aero_F[k] = EVDynamics.aero_F(
            self.ExtCond.rho, self.EV.A_front, self.EV.C_d, prev_speed)
        sol.roll_grade_F[k] = EVDynamics.roll_grade_F(max_veh_mass=self.EV.max_mass,
                                                      gravity_acc=Constants.g,
                                                      grade_angle=self.ExtCond.road_grade_angle)
        if np.abs(prev_speed) > 0:
            sol.roll_grade_F[k] = sol.roll_grade_F[k] + \
                self.EV.C_r * self.EV.max_mass * Constants.g
        sol.demand_torque[k] = EVDynamics.demand_torque(des_acc_F=sol.des_acc_F[k], aero_F=sol.aero_F[k],
                                                        roll_grade_F=sol.roll_grade_F[k],
                                                        road_F=self.ExtCond.road_force,
                                                        wheel_radius=self.EV.drive_train.wheel.r,
                                                        gear_ratio=self.EV.drive_train.gear_box.N)

        # The remaining calculations leads to actual speed
        # First check if demand torque is limited by the motor characteristics and calculate the max. torque and
        # limit torque
        if prev_motor_speed < self.EV.motor.RPM_r:
            sol.max_torque[k] = self.EV.motor.L_max
        else:
            sol.max_torque[k] = self.EV.motor.L_max * \
                self.EV.motor.RPM_r / prev_motor_speed

        sol.limit_regen[k] = np.minimum(
            sol.max_torque[k], self.EV.drive_train.frac_regen_torque * self.EV.motor.L_max)
        sol.limit_torque[k] = np.minimum(
            sol.demand_torque[k], sol.max_torque[k])
        if sol.limit_torque[k] > 0:
            sol.motor_torque[k] = sol.limit_torque[k]
        else:
            sol.motor_torque[k] = np.maximum(-sol.limit_regen[k],
                                             sol.limit_torque[k])

        # Now calculate the actual accelerations and speeds. Finally, the distance is calculated
        sol.actual_acc_F[k] = sol.limit_torque[k] * self.EV.drive_train.gear_box.N / self.EV.drive_train.wheel.r - \
            sol.aero_F[k] - sol.roll_grade_F[k] - self.ExtCond.road_force
        sol.actual_acc[k] = sol.actual_acc_F[k] / self.EV.equiv_mass
        sol.motor_speed[k] = np.minimum(self.EV.motor.RPM_max, self.EV.drive_train.gear_box.N * (
            prev_speed + sol.actual_acc[k] * (self.DriveCycle.t[k] - prev_time)) * 60 / (
            2 * np.pi * self.EV.drive_train.wheel.r))
        sol.actual_speed[k] = sol.motor_speed[k] * 2 * np.pi * self.EV.drive_train.wheel.r / (
            60 * self.EV.drive_train.gear_box.N)
        sol.actual_speed_kmph[k] = sol.actual_speed[k] * 3600 / 1000
        sol.distance[k] = prev_distance + ((sol.actual_speed_kmph[k] + prev_speed) / 2) * (self.DriveCycle.t[k] -
                                                                                      prev_time) / 3600

        # Finally, calculates the battery power, current demanded
        if sol.limit_torque[k] > 0:
            sol.demand_power[k] = sol.limit_torque[k]
        else:
            sol.demand_power[k] = np.maximum(
                sol.limit_torque[k], -sol.limit_regen[k])
        sol.demand_power[k] = (sol.demand_power[k] * 2 * np.pi) * \
            (prev_motor_speed + sol.motor_speed[k]) / (2 * 60000)
        sol.limit_power[k] = np.maximum(-self.EV.motor.P_max,
                                        np.minimum(self.EV.motor.P_max, sol.demand_power[k]))
        sol.battery_demand[k] = self.EV.overhead_power / 1000
        if sol.limit_power[k] > 0:
            sol.battery_demand[k] = sol.battery_demand[k] + \
                sol.limit_power[k] / self.EV.drive_train.eff
        else:
            sol.battery_demand[k] = sol.battery_demand[k] + \
                sol.limit_power[k] * self.EV.drive_train.eff
        sol.current[k] = sol.battery_demand[k] * 1000 / self.EV.pack.pack_V_nom
        sol.cell_current[k] = sol.current[k] / self.EV.pack.Np
        sol.battery_SOC[k] = prev_SOC - sol.current[k] * \
            (self.DriveCycle.t[k] - prev_time)

    def __repr__(self):
        return f"EVDynamics({self.EV}, {self.DriveCycle}, {self.ExtCond})"

    def __str__(self):
        return f"Vehicle Alias: {self.EV.alias_name} driving along {self.DriveCycle.drive_cycle_name}."
