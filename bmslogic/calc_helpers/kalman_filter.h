#include <vector>

class NormalRandomVector
{
public:
    NormalRandomVector(std::vector<std::vector<double>> vector_init, std::vector<std::vector<double>> cov_init);
    // getters
    std::vector<std::vector<double>> get_vec() const { return m_vec; }
    std::vector<std::vector<double>> get_cov() const { return m_cov; }
    size_t get_dim() { return m_vec.size(); }
    // setters
    void set_vec(std::vector<std::vector<double>> &i_vec) { m_vec = i_vec; }
    void set_cov(std::vector<std::vector<double>> &i_cov) { m_cov = i_cov; }

private:
    std::vector<std::vector<double>> m_vec;
    std::vector<std::vector<double>> m_cov;
};