"""
Tests for the extern c++ libraries
"""

import os
import pathlib
import unittest

import bmslogic.extern.extern as cpp_extern


# below gets the absoulute file path to the sample csv file
FILEPATH_TO_SAMPLE_CSV: str = os.path.join(pathlib.Path(__file__).parent.__str__(), "param_battery-cell.csv")

class TestHB(unittest.TestCase):
    df = cpp_extern.read_csv(FILEPATH_TO_SAMPLE_CSV, 0, 0)

    def test_get_index(self):
        self.assertEqual("Density [kg m^-3]", self.df.get_index[0])
        self.assertEqual("Volume [m^3]", self.df.get_index[1])
        self.assertEqual("Specific Heat [J K^-1 kg^-1]", self.df.get_index[2])
        self.assertEqual("Heat Transfer Coefficient [J s^-1 K^-1]", self.df.get_index[3])
        self.assertEqual("Surface Area [m^2]", self.df.get_index[4])
        self.assertEqual("Capacity [A hr]", self.df.get_index[5])
        self.assertEqual("Maximum Potential Cut-off [V]", self.df.get_index[6])
        self.assertEqual("Minimum Potential Cut-off [V]", self.df.get_index[7])

    def test_col_name(self):
        self.assertEqual("Value", self.df.get_colnames[0])
        self.assertEqual("Reference", self.df.get_colnames[1])

    def test_get_data(self):
        self.assertEqual('1626', self.df.get_data[0][0])
        self.assertEqual('Guo et al.', self.df.get_data[0][1])

        self.assertEqual('3.38E-05', self.df.get_data[1][0])
        self.assertEqual('Guo et al.', self.df.get_data[1][1])

        self.assertEqual('750', self.df.get_data[2][0])
        self.assertEqual('Guo et al.', self.df.get_data[2][1])

    def test_get_value(self):
        self.assertEqual("1626", self.df.get_value("Value", "Density [kg m^-3]"))

print(cpp_extern.read_csv(FILEPATH_TO_SAMPLE_CSV, 0, 0).get_data)

