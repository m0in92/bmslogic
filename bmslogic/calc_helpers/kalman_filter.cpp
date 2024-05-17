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
    m_nX = static_cast<int>(m_X.get_vec().size());
    m_nW = static_cast<int>(m_W.get_vec().size());
    m_nV = static_cast<int>(m_V.get_vec().size());
}

/**
 * @brief creates a augmented state row vector 
 * 
 * @return std::vector<std::vector<double>> 
 */
std::vector<std::vector<double>> SigmaPointKalmanFilter::aug_vec()
{
    std::vector<std::vector<double>> result = m_X.get_vec();

    // append the W vector
    for (size_t i = 0; i < m_W.get_dim(); i++)
    {
        result.push_back(m_W.get_vec()[i]);
    }

    // appends the V vector
    for (size_t i = 0; i < m_V.get_dim(); i++)
    {
        result.push_back(m_V.get_vec()[i]);
    }

    return result;
}
