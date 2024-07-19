"""
This module contains some cyclers that are derived from the cycler classes from cpp_modules. 
"""

__all__ = ["HPPCCyler", "DSTCycler"]
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."
__status__ = "Deployed"

from typing import Callable

import numpy as np
import scipy
import scipy.interpolate

from bmslogic.simulations.cell import cell


class InterpolatedCustomCycler(cell.CustomCycler):
    def __init__(self, t_array: np.ndarray, current_array: np.ndarray, dt: float,
                 V_min: float, V_max: float,
                 soc_lib_min: float, soc_lib_max: float, soc_lib: float):
        func_exp: Callable = scipy.interpolate.interp1d(
            t_array, current_array, kind="nearest", fill_value="extrapolate")
        t_array_: np.ndarray = np.arange(t_array[0], t_array[-1], dt)
        I_array_: np.ndarray = func_exp(t_array_)
        super().__init__(t_array=t_array_, current_array=I_array_,
                         V_min=V_min, V_max=V_max,
                         soc_lib_min=soc_lib_min, soc_lib_max=soc_lib_max, soc_lib=soc_lib)


class HPPCCycler(cell.CustomCycler):
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

        super().__init__(t_array=t_array, current_array=current_array,
                         V_min=V_min, V_max=V_max,
                         soc_lib_min=soc_lib_min, soc_lib_max=soc_lib_max, soc_lib=soc_lib)


class DSTCycler(cell.CustomCycler):
    def __init__(self, cap_nom: float,
                 V_min: float, V_max: float, soc_min: float, soc_max: float, soc: float,
                 dst_step: int = 10) -> None:
        dt: float = 0.1
        t_array, current_array = self.generate_one_cycle(
            cap_nom=cap_nom, dt=dt)
        for i in range(dst_step-1):
            t_array_, current_array_ = self.generate_one_cycle(
                cap_nom=cap_nom, t_init=t_array[-1] + dt, dt=dt)
            t_array = np.hstack((t_array, t_array_))
            current_array = np.hstack((current_array, current_array_))

        super().__init__(t_array=t_array, current_array=current_array,
                         V_min=V_min, V_max=V_max,
                         soc_lib_min=soc_min, soc_lib_max=soc_max, soc_lib=soc)

    def generate_one_cycle(self, cap_nom: float, t_init: float = 0.0, dt: float = 0.1) -> tuple[np.ndarray, np.ndarray]:
        rest_time: float = 16  # [s]
        # First 3 cycles with small steps
        # First Cycle
        t_array1: np.ndarray = np.arange(t_init, t_init + 16 + dt, dt)  # rest
        t_array2: np.ndarray = np.arange(
            t_array1[-1] + dt, t_array1[-1] + 2 * dt + 28.0, dt)  # discharge at 0.43C
        t_array3: np.ndarray = np.arange(
            t_array2[-1] + dt, t_array2[-1] + 2 * dt + 11.0, dt)  # discharge at 0.85C
        t_array4: np.ndarray = np.arange(
            t_array3[-1] + dt, t_array3[-1] + 2 * dt + 9.0, dt)  # charge at 0.43C

        I_array1 = np.zeros(len(t_array1))
        I_array2 = -0.43 * cap_nom * np.ones(len(t_array2))
        I_array3 = -0.85 * cap_nom * np.ones(len(t_array3))
        I_array4 = 0.43 * cap_nom * np.ones(len(t_array4))

        t_array: np.ndarray = np.hstack(
            (t_array1, t_array2, t_array3, t_array4))
        current_array: np.ndarray = np.hstack(
            (I_array1, I_array2, I_array3, I_array4))

        # Repeat 2 more times
        for i in range(2):
            t_array1: np.ndarray = np.arange(
                t_array[-1] + dt, t_array[-1] + 16 + dt, dt)  # rest
            t_array2: np.ndarray = np.arange(
                t_array1[-1] + dt, t_array1[-1] + 2 * dt + 28.0, dt)  # discharge at 0.43C
            t_array3: np.ndarray = np.arange(
                t_array2[-1] + dt, t_array2[-1] + 2 * dt + 11.0, dt)  # discharge at 0.85C
            t_array4: np.ndarray = np.arange(
                t_array3[-1] + dt, t_array3[-1] + 2 * dt + 9.0, dt)  # charge at 0.43C

            I_array1 = np.zeros(len(t_array1))
            I_array2 = -0.43 * cap_nom * np.ones(len(t_array2))
            I_array3 = -0.85 * cap_nom * np.ones(len(t_array3))
            I_array4 = 0.43 * cap_nom * np.ones(len(t_array4))

            t_array: np.ndarray = np.hstack(
                (t_array, t_array1, t_array2, t_array3, t_array4))
            current_array: np.ndarray = np.hstack(
                (current_array, I_array1, I_array2, I_array3, I_array4))

        del t_array1, t_array2, t_array3, t_array4, I_array1, I_array2, I_array3, I_array4

        # Step with one blarge currents
        # Rest for 16 seconds
        t_array1: np.ndarray = np.arange(
            t_array[-1] + dt, t_array[-1] + 2 * dt + 35.0, dt)
        I_array1: np.ndarray = np.zeros(len(t_array1))
        # Discharge at 0.43C for 35s
        t_array2: np.ndarray = np.arange(
            t_array1[-1] + dt, t_array1[-1] + 2 * dt + 35.0, dt)
        I_array2: np.ndarray = -0.43 * cap_nom * np.ones(len(t_array2))
        # Discharge at 3.45C for 8s
        t_array3: np.ndarray = np.arange(
            t_array2[-1] + dt, t_array2[-1] + 2*dt + 8.0, dt)
        I_array3: np.ndarray = -3.45 * cap_nom * np.ones(len(t_array3))
        # Discharge at 2.16C for 23 seconds
        t_array4: np.ndarray = np.arange(
            t_array3[-1] + dt, t_array3[-1] + 2*dt + 23.0, dt)
        I_array4: np.ndarray = -2.16 * cap_nom * np.ones(len(t_array4))
        # charge at 0.89C for 7 seconds
        t_array5: np.ndarray = np.arange(
            t_array4[-1] + dt, t_array4[-1] + 2*dt + 7.0, dt)
        I_array5: np.ndarray = 0.89 * cap_nom * np.ones(len(t_array5))
        # discharge at 0.86C for 30 seconds
        t_array6: np.ndarray = np.arange(
            t_array5[-1] + dt, t_array5[-1] + 2*dt + 30.0, dt)
        I_array6: np.ndarray = -0.86 * cap_nom * np.ones(len(t_array6))
        # charge 1.76C for 8 seconds
        t_array7: np.ndarray = np.arange(
            t_array6[-1] + dt, t_array6[-1] + 2*dt + 8.0, dt)
        I_array7: np.ndarray = 1.76 * cap_nom * np.ones(len(t_array7))
        # rest for 7s
        t_array8: np.ndarray = np.arange(
            t_array7[-1] + dt, t_array7[-1] + 2*dt + 30.0, dt)
        I_array8: np.ndarray = np.zeros(len(t_array8))

        t_array: np.ndarray = np.hstack((t_array, t_array1, t_array2, t_array3,
                                         t_array4, t_array5, t_array6))
        current_array: np.ndarray = np.hstack((current_array, I_array1, I_array2, I_array3,
                                               I_array4, I_array5, I_array6))

        return t_array, current_array
