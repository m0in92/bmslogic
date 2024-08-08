#include "pybind11/pybind11.h"
#include "pybind11/functional.h"
#include "pybind11/eigen.h"

#include "hummingbird.h"
#include "kalman_filter.h"

namespace py = pybind11;

PYBIND11_MODULE(calc_helpers, m)
{
     m.doc() = "Contains the functionality to aid in the battery simuliations, including accessing parameters files and performing non-linear Sigma Point Kalman Filter";

     py::class_<HB::DataFrames>(m, "DataFrames")
         .def_property_readonly("get_index", &HB::DataFrames::getIndex)
         .def_property_readonly("get_colnames", &HB::DataFrames::getColNames)
         .def_property_readonly("get_data", &HB::DataFrames::getData)
         .def("get_value", &HB::DataFrames::getValue);

     m.def("read_csv", &HB::read_csv);

     py::class_<TwoStatesOneInputOneOutput>(m, "TwoStatesOneInputOneOutput")
         .def(py::init<double, double, double, double,
                       double, double,
                       std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)>,
                       std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)>>(),
              py::arg("state1_init"), py::arg("state2_init"), py::arg("cov_state1"), py::arg("cov_state1"),
              py::arg("cov_w"), py::arg("cov_v"),
              py::arg("state_equation"), py::arg("output_equation"))
         .def_property_readonly("state", &TwoStatesOneInputOneOutput::get_state)
         .def_property_readonly("cov", &TwoStatesOneInputOneOutput::get_cov)
         .def("solve_one_iteration", &TwoStatesOneInputOneOutput::solve_one_iteration,
              py::arg("input"), py::arg("y_true"))
         .def("solve", &TwoStatesOneInputOneOutput::solve,
              py::arg("input"), py::arg("y_true"));
}