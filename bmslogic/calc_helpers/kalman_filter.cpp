#include "kalman_filter.h"

NormalRandomVector::NormalRandomVector(std::vector<std::vector<double>> i_vec_init,
                                       std::vector<std::vector<double>> i_cov_init)
    : m_vec(i_vec_init), m_cov(i_cov_init)
{
}

SigmaPointKalmanFilter::SigmaPointKalmanFilter(NormalRandomVector i_X, NormalRandomVector i_W, NormalRandomVector i_V, int y_dim,
                                               std::function<NormalRandomVector(NormalRandomVector, NormalRandomVector, NormalRandomVector)> state_equation,
                                               std::function<NormalRandomVector(NormalRandomVector, NormalRandomVector, NormalRandomVector)> output_equation,
                                               std::string method_type) : m_X(i_X), m_W(i_W), m_V(i_V), m_y_dim(y_dim),
                                                                          m_state_equation(state_equation), m_output_equation(output_equation), m_method_type(method_type)
{
}
