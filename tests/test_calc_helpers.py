import unittest

import numpy as np

# from bmslogic.calc_helpers.calc_helpers import NormalRandomVector, SigmaPointKalmanFilter
from bmslogic.calc_helpers.matrix_operations import find_the_element_with_closest_number, interp1d


# def func_f(x_k, u_k, w_k):
#     return np.sqrt(5 + x_k) + w_k

# def func_h(x_k, u_k, v_k):
#     return x_k ** 3 + v_k


# class TestPyNormalRandomVector(unittest.TestCase):
#     mean = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]).reshape(-1, 1)
#     cov = np.ones(len(mean) ** 2).reshape(len(mean), len(mean))

#     def test_constructor(self):
#         rv = NormalRandomVector(vector_init=self.mean, cov_init=self.cov)
#         self.assertTrue(np.array_equal(self.mean, rv.get_vec))
#         self.assertTrue(np.array_equal(self.cov, rv.get_cov))
#         self.assertEqual(len(self.mean), rv.get_dim)


# class TestSPKFProperties(unittest.TestCase):
#     vector_x = np.array([2, 2]).reshape(-1, 1)
#     vector_w = np.array([0]).reshape(-1, 1)
#     vector_v = np.array([0]).reshape(-1, 1)

#     vector_x2 = np.array([2]).reshape(-1, 1)
#     vector_w2 = np.array([0]).reshape(-1, 1)
#     vector_v2 = np.array([0]).reshape(-1, 1)

#     cov_x = np.array([[2, 0], [0, 2]])
#     cov_w = np.array([[1]])
#     cov_v = np.array([[2]])

#     cov_x2 = np.array([[1]])
#     cov_w2 = np.array([[1]])
#     cov_v2 = np.array([[2]])

#     x = NormalRandomVector(vector_init=vector_x, cov_init=cov_x)
#     w = NormalRandomVector(vector_init=vector_w, cov_init=cov_w)
#     v = NormalRandomVector(vector_init=vector_v, cov_init=cov_v)

#     x2 = NormalRandomVector(vector_init=vector_x2, cov_init=cov_x2)
#     w2 = NormalRandomVector(vector_init=vector_w2, cov_init=cov_w2)
#     v2 = NormalRandomVector(vector_init=vector_v2, cov_init=cov_v2)

#     y_dim = 1

#     # @staticmethod
#     # def func_f(x_k, u_k, w_k):
#     #     return np.sqrt(5 + x_k) + w_k

#     # @staticmethod
#     # def func_h(x_k, u_k, v_k):
#     #     return x_k ** 3 + v_k

#     spkf_instance: SigmaPointKalmanFilter = SigmaPointKalmanFilter(X=x, W=w, V=v, y_dim=y_dim,
#                                                                    state_equation=func_f, output_equation=func_h)
#     spkf_instance2: SigmaPointKalmanFilter = SigmaPointKalmanFilter(X=x2, W=w2, V=v2, y_dim=y_dim,
#                                                                     state_equation=func_f, output_equation=func_h)
    
#     def test_constructor(self):
#         self.assertTrue(np.array_equal(self.vector_x, np.array(self.spkf_instance.X.get_vec)))
#         self.assertTrue(np.array_equal(self.vector_w, self.spkf_instance.W.get_vec))
#         self.assertTrue(np.array_equal(self.vector_v, self.spkf_instance.V.get_vec))

#         self.assertEqual(2, self.spkf_instance.nX)
#         self.assertEqual(1, self.spkf_instance.nW)
#         self.assertEqual(1, self.spkf_instance.nV)

#         self.assertEqual(1, self.spkf_instance2.nX)
#         self.assertEqual(1, self.spkf_instance2.nW)
#         self.assertEqual(1, self.spkf_instance2.nV)

#     def test_aug_vector(self):
#         self.assertTrue(np.array_equal(np.array([2, 2, 0, 0]).reshape(-1, 1), self.spkf_instance.aug_vec()))


class TestClosestElement(unittest.TestCase):
    def test_case_1(self):
        array: np.ndarray = np.arange(0, 10, 1)
        value: float = 4.45

        self.assertEqual(4, find_the_element_with_closest_number(value=value, array=array)[0])
        self.assertEqual(4, find_the_element_with_closest_number(value=value, array=array)[1])


class TestInterp1d(unittest.TestCase):
    def test_case_1(self):
        array_1: np.ndarray = np.array([0,4,5,3,2])
        array_2: np.ndarray = np.array([10, 90, 67, 34, 98])
        
        self.assertEqual(10, interp1d(array_1=array_1, array_2=array_2, value=-10))
        self.assertEqual(78.5, interp1d(array_1=array_1, array_2=array_2, value=4.5))
        self.assertEqual(67, interp1d(array_1=array_1, array_2=array_2, value=100))
