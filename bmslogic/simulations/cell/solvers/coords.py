"""
Contains classes and functionalities pertaining to the co-ordinate system.
"""

__all__ = ['PyElectrolyteFVMCoordinates', 'PyFVMCoordinates', 'PyFDMCoordinates']

__authors__ = "Moin Ahmed"
__copyright__ = "Copyright by BMSLogic. All Rights Reserved."
__status__ = "deployed"


from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


@dataclass
class PyElectrolyteFVMCoordinates:
    """
    Stores the co-ordinates points for the 1D FVM simulations pertaining to electrolyte.
    """

    L_p: float  # thickness of the positive electrode region [m]
    L_s: float  # thickness of the seperator region [m]
    L_n: float  # thickness of the negative electrode region [m]

    num_grid_p: int = 10  # number of finite volumes in positive electrode region
    num_grid_s: int = 10  # number of finite volumes in the seperator region
    num_grid_n: int = 10  # number of finite volumes in the negative electrode region

    def __post_init__(self):
        self.dx_n = self.L_n / self.num_grid_n  # dx in the negative electrode region
        self.dx_s = self.L_s / self.num_grid_s  # dx in the seperator region
        self.dx_p = self.L_p / self.num_grid_p  # dx in the positive electrode region

    @property
    def array_x_n(self) -> np.ndarray:
        """
        Returns the location of center of the finite volumes in the negative electrode region.
        :return: array containing the centers of the finite volumes.
        """
        return np.arange(self.dx_n/2, self.L_n, self.dx_n)

    @property
    def array_x_s(self) -> np.ndarray:
        """
        Array containing the location of the nodes in the finite volume in the seperator region.
        :return: Array containing the location of the nodes in the finite volume in the seperator region.
        """
        return np.arange(self.L_n + self.dx_s/2, self.L_n + self.L_s, self.dx_s)

    @property
    def array_x_p(self) -> np.ndarray:
        """
        Array containing the locations of the center of the finite volumes in the positive electrode region.
        :return: Array containing the locations of the center of the finite volumes in the positive electrode region.
        """
        return np.arange(self.L_n + self.L_s + self.dx_p/2, self.L_n + self.L_s + self.L_p, self.dx_p)

    @property
    def array_x(self) -> np.ndarray:
        """
        Array containing the locations of the center of the finite volumes.
        :return: Array containing the locations of the center of the finite volumes.
        """
        return np.append(np.append(self.array_x_n, self.array_x_s), self.array_x_p)

    @property
    def array_dx(self) -> np.ndarray:
        """
        Array containing the width of the finite volumes.
        :return: Array containing the width of the finite volumes.
        """
        array_dx_n = self.dx_n * np.ones(len(self.array_x_n))
        array_dx_s = self.dx_s * np.ones(len(self.array_x_s))
        array_dx_p = self.dx_p * np.ones(len(self.array_x_p))
        return np.append(np.append(array_dx_n, array_dx_s), array_dx_p)


@dataclass
class PyFVMCoordinates(PyElectrolyteFVMCoordinates):
    pass


@dataclass
class PyFDMCoordinates:
    """
    Class that stores the spatial co-ordinates for the finite difference methods as Numpy arrays.
    """

    L_p: float  # thickness of the positive electrode region [m]
    L_s: float  # thickness of the seperator region [m]
    L_n: float  # thickness of the negative electrode region [m]

    num_grid_p: int = 10  # number of finite volumes in positive electrode region
    num_grid_s: int = 10  # number of finite volumes in the seperator region
    num_grid_n: int = 10  # number of finite volumes in the negative electrode region

    def __post_init__(self):
        self.dx_n = self.L_n / self.num_grid_n  # dx in the negative electrode region
        self.dx_s = self.L_s / self.num_grid_s  # dx in the seperator region
        self.dx_p = self.L_p / self.num_grid_p  # dx in the positive electrode region

    @property
    def array_x_n(self) -> np.ndarray:
        return np.linspace(0, self.L_n, self.num_grid_n)

    @property
    def array_x_s(self) -> np.ndarray:
        return np.arange(self.L_n, self.L_s + self.dx_s, self.dx_s)

    @property
    def array_x_p(self) -> np.ndarray:
        return np.arange(self.L_n + self.L_s, self.L_n + self.L_s + self.L_p + self.dx_p, self.dx_p)

    @property
    def array_x(self) -> np.ndarray:
        return np.append(self.array_x_p, np.append(self.array_x_s, self.array_x_p))

    @property
    def array_dx(self) -> np.ndarray:
        array_dx_n = self.dx_n * np.ones(self.num_grid_n)
        array_dx_s = self.dx_s * np.ones(self.num_grid_s)
        array_dx_p = self.dx_p * np.ones(self.num_grid_p)
        return np.append(array_dx_n, np.append(array_dx_s, array_dx_p))


