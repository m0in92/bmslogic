#include <functional>
#include <vector>

#include "pybind11/pybind11.h"
#include "pybind11/functional.h"
#include "pybind11/stl.h"

#include "kalman_filter.h"

namespace py = pybind11;

PYBIND11_MODULE(calc_helpers, m)
{
    m.doc() = "Contains the functions and classes that aid in the simulation calculations.";

    // Normal Random Vector
    py::class_<NormalRandomVector>(m, "NormalRandomVector")
        .def(py::init<std::vector<std::vector<double>>, std::vector<std::vector<double>>>(), py::arg("vector_init"), py::arg("cov_init"))
        .def_property("get_vec", &NormalRandomVector::get_vec, &NormalRandomVector::set_vec)
        .def_property("get_cov", &NormalRandomVector::get_cov, &NormalRandomVector::set_cov)
        .def_property_readonly("get_dim", &NormalRandomVector::get_dim);

    // Sigma Point Kalman Filter
    py::class_<SigmaPointKalmanFilter>(m, "SigmaPointKalmanFilter")
        .def(py::init<NormalRandomVector, NormalRandomVector, NormalRandomVector, int,
                      std::function<NormalRandomVector(NormalRandomVector, NormalRandomVector, NormalRandomVector)>,
                      std::function<NormalRandomVector(NormalRandomVector, NormalRandomVector, NormalRandomVector)>,
                      std::string>(),
                      py::arg("X"), py::arg("W"), py::arg("V"), py::arg("y_dim"), 
                      py::arg("state_equation"), py::arg("output_equation"), py::arg("method_type")="CDKF")
        .def_property_readonly("X", &SigmaPointKalmanFilter::get_X)
        .def_property_readonly("W", &SigmaPointKalmanFilter::get_W)
        .def_property_readonly("V", &SigmaPointKalmanFilter::get_V);
}
