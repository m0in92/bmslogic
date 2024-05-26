"""
Contains the functionalities pertaining to battery cell cycler objects in Python programming language.
"""

__all__ = ['PyBaseCycler', 
           'PyCC', 'PyCCNoFirstRest', 'PyCCCV', 'PyDischargeRestCharge', 'PyDischargeRestChargeRest', 'PyCharge', 'PyChargeRest'
           'PyDischarge', 'PyDischargeRest', 'PyCustomDischarge', 'PyCustomCycler', 'PyHPPCCycler']
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by Moin Ahmed. All Rights Reserved."
__status__ = "Deployed"

from dataclasses import dataclass, field
from abc import ABC, abstractmethod

import numpy as np
import numpy.typing as npt
from scipy import interpolate
import matplotlib.pyplot as plt



@dataclass
class PyBaseCycler(ABC):
    time_elapsed: float = field(default=0.0)  # time elapsed during cycling
    SOC_LIB: float = field(default=0.0)  # present battery cell SOC
    SOC_LIB_min: float = field(default=0.0)  # minimum battery cell SOC
    SOC_LIB_max: float = field(default=1.0)  # maximum battery cell SOC
    charge_current: float = field(default=0.0)  # charge current [A]
    discharge_current: float = field(default=0.0)  # discharge current [A]
    rest_time: float = field(default=0.0)  # rest time for the step "rest" [s]
    v_min: float = field(default=2.0)
    v_max: float = field(default=4.2)

    num_cycles: int = field(default=0)  # number of cycles
    cycle_steps: list = field(default_factory=lambda: [])  # list containing the sequence of the steps in a cycle

    @abstractmethod
    def get_current(self, step_name: str, t: float) -> float:
        """
        Returns the current for a particular cycling step. It is only valid for constant current situations.
        :param step_name: (string) The cycling step name.
        :param t: (float) the time value at the current time step [s]
        :return: (double) The current value.
        """
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    # @abstractmethod
    def reset(self) -> None:
        """
        Resets the cycler instance.
        :return:
        """
        self.time_elapsed = 0.0


class PyCC(PyBaseCycler):
    # class variables
    cycle_steps = ["rest", "charge", "rest", "discharge"]

    def __init__(self, num_cycles: int,
                 charge_current: float, discharge_current: float, rest_time: float,
                 V_max: float, V_min: float):
        super().__init__()
        self.num_cycles = num_cycles
        self.charge_current = charge_current
        self.discharge_current = -discharge_current
        self.rest_time = rest_time
        self.V_max = V_max
        self.V_min = V_min

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class PyCCNoFirstRest(PyBaseCycler):
    # class variables
    cycle_steps = ["charge", "rest", "discharge", "rest"]

    def __init__(self, num_cycles, charge_current, discharge_current, rest_time, V_max, V_min, SOC_min=0, SOC_max=1,
                 SOC_LIB=0):
        super().__init__()
        self.num_cycles = num_cycles
        self.charge_current = charge_current
        self.discharge_current = -discharge_current
        self.rest_time = rest_time
        self.V_max = V_max
        self.V_min = V_min
        self.SOC_min = SOC_min
        self.SOC_max = SOC_max
        self.SOC_LIB = SOC_LIB

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class PyCCCV(PyBaseCycler):
    # class variables
    cycle_steps = ["charge", "CV", "rest", "discharge", "rest"]

    def __init__(self, num_cycles, charge_current, discharge_current, rest_time, V_max, V_min, SOC_min=0, SOC_max=1,
                 SOC_LIB=0):
        super().__init__()
        self.num_cycles = num_cycles
        self.charge_current = charge_current
        self.discharge_current = -discharge_current
        self.rest_time = rest_time
        self.V_max = V_max
        self.V_min = V_min
        self.SOC_min = SOC_min
        self.SOC_max = SOC_max
        self.SOC_LIB = SOC_LIB

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class PyDischargeRestCharge(PyBaseCycler):
    def __init__(self, discharge_current: float, rest_time: float, charge_current: float,
                 V_max: float, V_min: float,
                 SOC_LIB: float=1, SOC_LIB_min=0, SOC_LIB_max=1):
        super().__init__(SOC_LIB=SOC_LIB, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max)
        self.discharge_current = -discharge_current
        self.charge_current = charge_current
        self.V_max = V_max
        self.V_min = V_min
        self.SOC_LIB_init = SOC_LIB
        self.rest_time = rest_time
        self.cycle_steps = ['discharge', 'rest', 'charge']
        self.num_cycles = 1

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class PyDischargeRestChargeRest(PyBaseCycler):
    def __init__(self, num_cycles: float, discharge_current: float, rest_time: float, charge_current: float,
                 V_max: float, V_min: float,
                 SOC_LIB: float=1, SOC_LIB_min=0, SOC_LIB_max=1):
        super().__init__(SOC_LIB=SOC_LIB, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max, num_cycles=num_cycles)
        self.discharge_current = -discharge_current
        self.charge_current = charge_current
        self.V_max = V_max
        self.V_min = V_min
        self.SOC_LIB_init = SOC_LIB
        self.rest_time = rest_time
        self.cycle_steps = ['discharge', 'rest', 'charge', 'rest']
        self.num_cycles = 1

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class PyCharge(PyBaseCycler):
    def __init__(self, charge_current: float, V_max: float, SOC_LIB_max: float=1, SOC_LIB: float=0):
        super().__init__(charge_current=charge_current, SOC_LIB_max=SOC_LIB_max)
        # self.charge_current = charge_current
        self.V_max = V_max
        self.num_cycles = 1
        # self.SOC_max = SOC_max
        self.SOC_LIB = SOC_LIB
        self.cycle_steps = ['charge']
        self.SOC_LIB_init = SOC_LIB

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        return self.charge_current

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class PyChargeRest(PyBaseCycler):
    def __init__(self, charge_current: float, rest_time: float, V_max:float, SOC_LIB_max:float=1, SOC_LIB:float=0):
        super().__init__(charge_current=charge_current, SOC_LIB_max=SOC_LIB_max, SOC_LIB=SOC_LIB)
        self.cycle_steps = ['charge', 'rest']
        self.rest_time = rest_time
        self.num_cycles = 1
        self.V_max = V_max
        self.SOC_LIB_init = SOC_LIB

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == 'charge':
            return self.charge_current
        elif step_name == 'rest':
            return 0.0

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class PyDischarge(PyBaseCycler):
    def __init__(self, discharge_current: float, v_min: float, SOC_LIB_min: float, SOC_LIB: float):
        super().__init__(SOC_LIB_min=SOC_LIB_min, SOC_LIB=SOC_LIB)
        self.discharge_current = -discharge_current
        self.v_min = v_min
        self.num_cycles = 1
        self.cycle_steps = ['discharge']
        self.SOC_LIB_init = SOC_LIB

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        return self.discharge_current

    def reset(self) -> None:
        self.time_elapsed = 0
        self.SOC_LIB = self.SOC_LIB_init


class PyDischargeRest(PyBaseCycler):
    def __init__(self, discharge_current, rest_time, V_min, SOC_LIB_min, SOC_LIB, SOC_LIB_max):
        super().__init__(SOC_LIB=SOC_LIB, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max)
        self.discharge_current = -discharge_current
        self.rest_time = rest_time
        self.V_min = V_min
        self.num_cycles = 1
        self.cycle_steps = ['discharge', 'rest']
        self.SOC_LIB_init = SOC_LIB

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == 'discharge':
            return self.discharge_current
        elif step_name == 'rest':
            return 0

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class PyCustomDischarge(PyBaseCycler):
    def __init__(self, t_array, I_array, V_min):
        # Check for input type.
        if not isinstance(t_array, np.ndarray):
            raise TypeError("t_array needs to be a numpy array.")
        if not isinstance(I_array, np.ndarray):
            raise TypeError("I_array needs to be a numpy array.")
        # Check is the size of the time and current arrays are equal
        if len(t_array) != len(I_array):
            raise ValueError("t_array and I_array needs to be of the same length.")
        super().__init__()
        self.t_array = t_array
        self.t_max = t_array[-1] # maximum time
        self.I_array = -I_array
        self.V_min = V_min
        self.charge_current = 0.0
        self.num_cycles = 1
        self.cycle_steps = ['discharge']

    def get_current(self, step_name: str, t_input: float) -> float:
        """
        This method returns the current at the given time. This method overwrites the Base charger's respective method.
        :param step_name: The step name.
        :param t_input: time input.
        :return: The value of the current.
        """
        if step_name == "discharge":
            # find the index in t_array that matches the t_input
            t_index = np.where(self.t_array == t_input)
            # find the index in t_array that matches the t_input
            if np.any(t_index):
                return self.I_array[t_index][0]
            else:
                return 0.0
        else:
            return 0.0
        

class PyCustomCycler(PyBaseCycler):
    def __init__(self, array_t: npt.ArrayLike, array_I: npt.ArrayLike, V_min: float, V_max: float,
                 SOC_LIB: float=1.0, SOC_LIB_min: float=0.0, SOC_LIB_max: float=1.0):
        """
        CustomCycler constructor.
        :param t_array: numpy array containing the time values in sequence [s].
        :param I_array: numpy array containing the current values.
        :param SOC_LIB:
        """
        super().__init__(SOC_LIB=SOC_LIB, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max)
        # check is t_array and I_array are numpy arrays.
        if (not isinstance(array_t, np.ndarray)) and (not isinstance(array_I, np.ndarray)):
            raise TypeError("t_array and I_array needs to be a numpy array.")

        # t_array and I_array needs to be of equal sizes
        if array_t.shape[0] != array_I.shape[0]:
            raise ValueError("t_array and I_array are not of equal sizes.")

        self.array_t = array_t
        self.array_I = array_I
        self.cycle_steps = ['custom']
        self.SOC_LIB_init = self.SOC_LIB
        self.V_min = V_min
        self.V_max = V_max

    @property
    def t_max(self):
        """
        Returns the time value at the last iteration.
        :return: (float) time value at the last iteration
        """
        return self.array_t[-1]

    def get_current(self, step_name: str, t: float) -> float:
        """
        Returns the current value from the inputted time value. This current value is interpolation based on the
        current value at the previous time step.
        :param step_name: cycling step name
        :param t: time [s]
        :returns: current value [A]
        """
        i_app = interpolate.interp1d(self.array_t, self.array_I, kind='previous', fill_value='extrapolate')(t)
        if np.isnan(i_app):
            return 0.0
        return i_app

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init

    def plot(self):
        """
        Plots the cycler's instance time [s] vs. current [A]. According to the convention, the discharge current is
        negative.
        :return:
        """
        plt.plot(self.array_t, self.array_I)
        plt.xlabel('Time [s]')
        plt.ylabel('I [A]')
        plt.show()


class PyHPPCCycler(PyCustomCycler):
    def __init__(self, t1: float, t2: float, i_app: float, charge_or_discharge: str,
                 V_min: float, V_max: float,
                 soc_lib_min: float, soc_lib_max: float, soc_lib: float,
                 hppc_steps: int = 10) -> None:
        """intended to be the cycler class for HPPC experiments. HPPC defined here has the following profile
                1. Rest for t1
                2. Current pulse, with the amplitude of i_app, for a time period of t2. THh current is negative if
                    the battery cell is discharging and positive if is charging.
                3. Repeat steps 1 and 2 until the desired terminal voltage is attained

        Args:
            t1 (float): time period [s] for the initial rest and between the current pulse
            t2 (float): time period [s] of the current pulse
            current (float): current value [A] during the pulse
            charge_or_discharge (str): options are 'charge' or 'discharge'
            V_min (float): minimum terminal voltage [V]
            V_max (float): maximum terminal voltage [V]
            soc_lib_min (float): minimum LIB SOC
            soc_lib_max (float): max. LIB SOC
            soc_lib (float): SOC LIB at the start of the HPPC cycling step.
            hppc_steps (int): number of HPPC repetitions. DEfault is 10.
        """
        dt: float = 0.1  # the time difference between the time steps
        if charge_or_discharge == 'discharge':
            i_app_actual: float = -i_app
        elif charge_or_discharge == 'charge':
            i_app_actual: float = i_app
        else:
            raise ValueError(
                f"input for charge_discharge parameter, {charge_or_discharge}, cannot be reconigized.")

        # This is the first iteration of the HPPC cycler
        t1_array: np.ndarray = np.arange(0, t1, dt)
        i_app1_array: np.ndarray = np.zeros(len(t1_array))
        t2_array: np.ndarray = np.arange(t1, t1+t2+dt, dt)
        i_app2_array: np.ndarray = i_app_actual * np.ones(len(t2_array))

        t_array: np.ndarray = np.append(t1_array, t2_array)
        current_array: np.ndarray = np.append(i_app1_array, i_app2_array)

        # This is the successive iteration of the HPPC cycler. Alternatively, the first and successive iterations
        # could have been coded into one iteration by introducing an empty t_array and current_array. However,
        # this lead to unpredictable behaviour in numpy arrays.
        for i in range(hppc_steps-1):
            t1_array: np.ndarray = np.arange(
                t_array[-1] + dt, t_array[-1] + t1, dt)
            i_app1_array: np.ndarray = np.zeros(len(t1_array))
            t2_array: np.ndarray = np.arange(
                t_array[-1] + t1, t_array[-1] + t1 + t2 + dt, dt)
            i_app2_array: np.ndarray = i_app_actual * np.ones(len(t2_array))

            t_array: np.ndarray = np.append(t_array, t1_array)
            t_array: np.ndarray = np.append(t_array, t2_array)
            current_array: np.ndarray = np.append(current_array, i_app1_array)
            current_array: np.ndarray = np.append(current_array, i_app2_array)

        super().__init__(array_t=t_array, array_I=current_array,
                         V_min=V_min, V_max=V_max,
                         SOC_LIB_min=soc_lib_min, SOC_LIB_max=soc_lib_max, SOC_LIB=soc_lib)