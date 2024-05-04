"""
Unittests for Solution and Plots
"""
__all__ = ["TestSolutionClass"]
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."
__status__ = "Developement"

import unittest

import numpy as np

import build.bmslogic.simulations.cell.Debug.cell as slv


class TestSolutionClass(unittest.TestCase):
    """
    Class to test the functionalities of the Solution class.
    """
    t: np.ndarray = np.linspace(0, 10, 10)
    cycling_step = np.chararray(len(t), itemsize=10)
    cycling_step[:] = "discharge"
    V: np.ndarray = 3.8 * np.ones(len(t))
    temp: np.ndarray = 298.15 * np.ones(len(t))
    cap: np.ndarray = 1e-5 * np.ones(len(t))
    soc_n: np.ndarray = 0.7 * np.ones(len(t))
    soc_p: np.ndarray = 0.5 * np.ones(len(t))
    blank_sol: slv.Solution = slv.Solution(t=np.array([]),
                                           cycling_step=np.array([]),
                                           V=np.array([]),
                                           temp = np.array([]),
                                           cap=np.array([]),
                                           soc_p=np.array([]),
                                           soc_n=np.array([]))
    filled_sol: slv.Solution = slv.Solution(t=t,
                                            cycling_step=cycling_step,
                                            V=V,
                                            temp=temp,
                                            cap=cap,
                                            soc_p=soc_p,
                                            soc_n=soc_n)

    def test_properties_getters(self) -> None:
        self.assertTrue(np.array_equal(self.t, self.filled_sol.t))
        self.assertTrue(np.array_equal(self.V, self.filled_sol.V))
        self.assertTrue(np.array_equal(self.temp, self.filled_sol.temp))
        self.assertTrue(np.array_equal(self.cap, self.filled_sol.cap))
        self.assertTrue(np.array_equal(self.soc_p, self.filled_sol.soc_p))
        self.assertTrue(np.array_equal(self.soc_n, self.filled_sol.soc_n))


# class TestPlot(unittest.TestCase):
#     t: np.ndarray = np.linspace(0, 10, 10)
#     cycling_step = np.chararray(len(t), itemsize=10)
#     cycling_step[:] = "discharge"
#     V: np.ndarray = 3.8 * np.ones(len(t))
#     temp: np.ndarray = 298.15 * np.ones(len(t))
#     cap: np.ndarray = 1e-5 * np.ones(len(t))
#     soc_n: np.ndarray = 0.7 * np.ones(len(t))
#     soc_p: np.ndarray = 0.5 * np.ones(len(t))

#     sol: slv.Solution = slv.Solution(t=t, 
#                                      cycling_step=cycling_step,
#                                      V=V,
#                                      temp=temp,
#                                      cap=cap,
#                                      soc_p=soc_p,
#                                      soc_n=soc_n)

#     plots_instance: slv.plot = slv.Plot(sol=sol)

#     def test_method_get_attribute(self):
#         attribute_name_1: str = self.plots_instance.get_attributes()[0]
#         for attribute_name in self.plots_instance.get_attributes():
#             self.assertTrue(self.check_attribute(attribute_name=attribute_name), msg=f"Couldn't find attribute {attribute_name}.")

#     def check_attribute(self, attribute_name: str) -> bool:
#         """Checks if the input parameter string is hand-coded attribute names.  

#         Parameters
#         ----------
#         attribute_name : str
#             attribute_name to check

#         Returns
#         -------
#         bool
#             True if the input attribute name is an class's instance attribute name.
#         """
#         return_bool: bool = False
#         attribute_names: list = ["t", "cycling_step", "sol", "V", "temp", "cap", "soc_p", "soc_n"]
#         if attribute_name in attribute_names:
#             return_bool = True
#         return return_bool


