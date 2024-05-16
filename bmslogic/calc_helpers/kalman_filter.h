#include <functional>
#include <string>
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

class SigmaPointKalmanFilter
{
public:
    SigmaPointKalmanFilter(NormalRandomVector i_X, NormalRandomVector i_W, NormalRandomVector i_V, int y_dim,
                           std::function<NormalRandomVector(NormalRandomVector, NormalRandomVector, NormalRandomVector)> state_equation,
                           std::function<NormalRandomVector(NormalRandomVector, NormalRandomVector, NormalRandomVector)> output_equation,
                           std::string method_type);

    // getters
    NormalRandomVector get_X() { return m_X; }
    NormalRandomVector get_W() { return m_W; }
    NormalRandomVector get_V() { return m_V; }

private:
    NormalRandomVector m_X;
    NormalRandomVector m_W;
    NormalRandomVector m_V;

    int m_y_dim;
    size_t m_mX = m_X.get_vec().size(); // size of vector X
    size_t m_mW = m_X.get_vec().size(); // size of vector W
    size_t m_mV = m_X.get_vec().size(); // size of vector V
    int L;                              // dimensions of augmented covariance state vector
    int p;                              // number of Sigma Points

    std::function<NormalRandomVector(NormalRandomVector, NormalRandomVector, NormalRandomVector)> m_state_equation;
    std::function<NormalRandomVector(NormalRandomVector, NormalRandomVector, NormalRandomVector)> m_output_equation;

    std::string m_method_type;
};