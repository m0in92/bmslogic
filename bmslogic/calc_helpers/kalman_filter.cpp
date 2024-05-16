#include "kalman_filter.h"

NormalRandomVector::NormalRandomVector(std::vector<std::vector<double>> i_vec_init,
                                       std::vector<std::vector<double>> i_cov_init)
    : m_vec(i_vec_init), m_cov(i_cov_init)
{
}
