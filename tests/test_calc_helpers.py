import unittest

import numpy as np

from bmslogic.calc_helpers.calc_helpers import NormalRandomVector


class TestPyNormalRandomVector(unittest.TestCase):
    mean = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]).reshape(-1, 1)
    cov = np.ones(len(mean) ** 2).reshape(len(mean), len(mean))

    def test_constructor(self):
        rv = NormalRandomVector(vector_init=self.mean, cov_init=self.cov)
        self.assertTrue(np.array_equal(self.mean, rv.get_mean))
        self.assertTrue(np.array_equal(self.cov, rv.get_cov))
        self.assertEqual(len(self.mean), rv.get_dim)

