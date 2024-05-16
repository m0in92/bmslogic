#include <vector>

#include "pybind11/pybind11.h"
#include "pybind11/stl.h"

#include "kalman_filter.h"

namespace py = pybind11;

PYBIND11_MODULE(calc_helpers, m)
{
    m.doc() = "Contains the functions and classes that aid in the simulation calculations.";

    py::class_<NormalRandomVector>(m, "NormalRandomVector")
        .def(py::init<std::vector<std::vector<double>>, std::vector<std::vector<double>>>(), py::arg("vector_init"), py::arg("cov_init"))
        .def_property("get_mean", &NormalRandomVector::get_vec, &NormalRandomVector::set_vec)
        .def_property("get_cov", &NormalRandomVector::get_cov, &NormalRandomVector::set_cov)
        .def_property_readonly("get_dim", &NormalRandomVector::get_dim);
}
