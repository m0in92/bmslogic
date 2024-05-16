import unittest

import numpy as np

from bmslogic.calc_helpers.calc_helpers import NormalRandomVector, SigmaPointKalmanFilter


def func_f(x_k, u_k, w_k):
    return np.sqrt(5 + x_k) + w_k

def func_h(x_k, u_k, v_k):
    return x_k ** 3 + v_k


class TestPyNormalRandomVector(unittest.TestCase):
    mean = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]).reshape(-1, 1)
    cov = np.ones(len(mean) ** 2).reshape(len(mean), len(mean))

    def test_constructor(self):
        rv = NormalRandomVector(vector_init=self.mean, cov_init=self.cov)
        self.assertTrue(np.array_equal(self.mean, rv.get_vec))
        self.assertTrue(np.array_equal(self.cov, rv.get_cov))
        self.assertEqual(len(self.mean), rv.get_dim)


class TestSPKFProperties(unittest.TestCase):
    vector_x = np.array([2, 2]).reshape(-1, 1)
    vector_w = np.array([0]).reshape(-1, 1)
    vector_v = np.array([0]).reshape(-1, 1)

    vector_x2 = np.array([2]).reshape(-1, 1)
    vector_w2 = np.array([0]).reshape(-1, 1)
    vector_v2 = np.array([0]).reshape(-1, 1)

    cov_x = np.array([[2, 0], [0, 2]])
    cov_w = np.array([[1]])
    cov_v = np.array([[2]])

    cov_x2 = np.array([[1]])
    cov_w2 = np.array([[1]])
    cov_v2 = np.array([[2]])

    x = NormalRandomVector(vector_init=vector_x, cov_init=cov_x)
    w = NormalRandomVector(vector_init=vector_w, cov_init=cov_w)
    v = NormalRandomVector(vector_init=vector_v, cov_init=cov_v)

    x2 = NormalRandomVector(vector_init=vector_x2, cov_init=cov_x2)
    w2 = NormalRandomVector(vector_init=vector_w2, cov_init=cov_w2)
    v2 = NormalRandomVector(vector_init=vector_v2, cov_init=cov_v2)

    y_dim = 1

    # @staticmethod
    # def func_f(x_k, u_k, w_k):
    #     return np.sqrt(5 + x_k) + w_k

    # @staticmethod
    # def func_h(x_k, u_k, v_k):
    #     return x_k ** 3 + v_k

    spkf_instance: SigmaPointKalmanFilter = SigmaPointKalmanFilter(X=x, W=w, V=v, y_dim=y_dim,
                                                                   state_equation=func_f, output_equation=func_h)
    spkf_instance2: SigmaPointKalmanFilter = SigmaPointKalmanFilter(X=x2, W=w2, V=v2, y_dim=y_dim,
                                                                    state_equation=func_f, output_equation=func_h)
    
    def test_constructor(self):
        self.assertTrue(np.array_equal(self.vector_x, np.array(self.spkf_instance.X.get_vec)))
        self.assertTrue(np.array_equal(self.vector_w, self.spkf_instance.W.get_vec))
        self.assertTrue(np.array_equal(self.vector_v, self.spkf_instance.V.get_vec))
        # self.assertEqual(self.y_dim, self.spkf_instance.y_dim)
