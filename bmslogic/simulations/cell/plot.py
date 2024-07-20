"""
Contains the plotting/visualization objects.
"""

__author__ = "Moin Ahmed"
__copyright__ = 'Copyright 2024 by BMSLogic. All rights reserved.'
__status__ = 'Deployed'

__all__ = ['Plot']

import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl

import bmslogic.simulations.cell.cell as cell_sim
# from SPCPPY.calc_helpers import constants


class Plot:
    def __init__(self, sol: cell_sim.Solution) -> None:
        """Constructor for the Plot class

        Args:
            sol (cell.Solution): sp.Solution object obtained after the simulation.
        """
        self.t: list = sol.t  # Array containing the times at each timesteps [s]
        self.cycling_step = sol.cycling_step  # cycling step type, for example "discharge", "charge", "rest"
        self.V: list = sol.V  # array containing the voltage at each timesteps [V]
        self.temp: list = sol.temp  # array of batterycell surface temperature [K]
        self.cap: list = sol.cap  # array containing the battery's capacity during a cycling step.
        self.soc_p: list = sol.soc_p  # array containing the positive electrode soc at each time step.
        self.soc_n: list = sol.soc_n  # array containing the negative electrode soc at each time step.
        self.OCV_LIB: list = sol.OCV_LIB  # open-circuit potential of the battery cell

    def get_attributes(self) -> list:
        """Returns a list of instance attributes

        Returns
        -------
        list
            instance attributes.
        """
        return list(self.__dict__.keys())
    
    def filter_discharge_cap(self):
        """returns the discharge capacity [in Ahr]

        Returns
        -------
        list
            list containing the capacity from the discharge cycling step.
        """
        return [cap for index, cap in enumerate(self.cap) if self.cycling_step[index] == 'discharge']
    
    def filter_discharge_V(self):
        """returns the terminal voltage [in V] during discharge

        Returns
        -------
        list
            list containing the voltage [in Ahr] during discharge.
        """
        return [V_ for index, V_ in enumerate(self.V) if self.cycling_step[index] == 'discharge']
    
    def filter_charge_cap(self):
        return [cap for index, cap in enumerate(self.cap) if self.cycling_step[index] == 'charge']
    
    def filter_charge_V(self):
        return [V_ for index, V_ in enumerate(self.V) if self.cycling_step[index] == 'charge']
        
    def set_matplotlib_settings(self) -> None:
        """Defines the matplotlib settings.
        """
        mpl.rcParams['lines.linewidth'] = 3
        plt.rc('axes', titlesize=20)
        plt.rc('axes', labelsize=20)
        plt.rcParams['font.size'] = 15

    def plot_tV(self):
        plt.plot(self.t, self.V)
        plt.show()

    def plot_comprehensive_isothermal(self) -> None:
        """Generates subplots of battery simulation results.
        """
        num_rows: int = 2
        num_cols: int = 2
        fig = plt.figure(figsize=(6.4*2/2, 4.8*2/2), dpi=300)

        # t-V plot
        ax1 = fig.add_subplot(num_rows, num_cols, 1)
        ax1.plot(self.t, self.V)
        ax1.pot(self.t, self.OCV_LIB)
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('V [V]')
        ax1.set_title('V vs. Time')

        # cap-V plot
        ax2 = fig.add_subplot(num_rows, num_cols, 2)
        if "discharge" in np.unique(self.cycling_step):
            cap: list = self.filter_discharge_cap()
            V: list = self.filter_discharge_V()
        elif "charge" in np.unique(self.cycling_step):
            cap: list = self.filter_charge_cap()
            V: list = self.filter_charge_V()
        else:
            cap: list = self.cap
            V: list = self.V
        ax2.plot(cap, V)
        ax2.set_xlabel('Capacity [Ahr]')
        ax2.set_ylabel('V [V]')
        ax2.set_title('V vs. Capacity')
        ax2.legend()

        # t-soc_p plot
        ax3 = fig.add_subplot(num_rows, num_cols, 3)
        ax3.plot(self.t, self.soc_p)
        ax3.set_xlabel('Time [s]')
        ax3.set_ylabel('SOC')
        ax3.set_title('Positive Electrode SOC')

        # t-soc_n plot
        ax4 = fig.add_subplot(num_rows, num_cols, 4)
        ax4.plot(self.t, self.soc_n)
        ax4.set_xlabel('Time [s]')
        ax4.set_ylabel('SOC')
        ax4.set_title('Negative Electrode SOC')

        plt.tight_layout()
        plt.show()

    def plot_comprehensive(self) -> None:
        """Generates subplots of battery simulation results.
        """
        num_rows: int = 3
        num_cols: int = 2
        fig = plt.figure()

        # t-V plot
        ax1 = fig.add_subplot(num_rows, num_cols, 1)
        ax1.plot(self.t, self.V)
        ax1.plot(self.t, self.OCV_LIB, linestyle=":", linewidth=0.5, label="OCV")

        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('V [V]')
        ax1.set_title('V vs. Time')
        ax1.legend()

        # cap-V plot
        ax2 = fig.add_subplot(num_rows, num_cols, 2)
        if "discharge" in np.unique(self.cycling_step):
            cap: list = self.filter_discharge_cap()
            V: list = self.filter_discharge_V()
        elif "charge" in np.unique(self.cycling_step):
            cap: list = self.filter_charge_cap()
            V: list = self.filter_charge_V()
        else:
            cap: list = self.cap
            V: list = self.V
        ax2.plot(cap, V)
        ax2.set_xlabel('Capacity [Ahr]')
        ax2.set_ylabel('V [V]')
        ax2.set_title('V vs. Capacity')

        # t-soc_p plot
        ax3 = fig.add_subplot(num_rows, num_cols, 3)
        ax3.plot(self.t, self.soc_p)
        ax3.set_xlabel('Time [s]')
        ax3.set_ylabel('SOC')
        ax3.set_title('Positive Electrode SOC')

        # t-soc_n plot
        ax4 = fig.add_subplot(num_rows, num_cols, 4)
        ax4.plot(self.t, self.soc_n)
        ax4.set_xlabel('Time [s]')
        ax4.set_ylabel('SOC')
        ax4.set_title('Negative Electrode SOC')

        # t-temp
        ax5 = fig.add_subplot(num_rows, num_cols, 5)
        ax5.plot(self.t, np.array(self.temp))
        # ax5.plot(self.t, np.array(self.temp) - constants.Constants.T_abs)
        ax5.set_xlabel('Time [s]')
        ax5.set_ylabel('Temperature [C]')
        ax5.set_title('Battery Cell Surface Temp.')

        plt.tight_layout()
        plt.show()


