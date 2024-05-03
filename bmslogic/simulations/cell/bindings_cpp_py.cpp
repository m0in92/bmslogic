/**
 * @file bindings_cpp_py.cpp
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief contains the code to compile .so files pertaining to battery cell simulations
 * @version 0.1
 * @date 2024-05-03
 *
 * @copyright Copyright (c) 2024
 *
 */

#include <string>

#include "pybind11/pybind11.h"
#include "pybind11/functional.h"
#include "pybind11/stl.h"

#include "battery_components.h"

namespace py = pybind11;

PYBIND11_MODULE(cell, m)
{
    // py::class_<Electrode>(m, "Electrode")
    //     .def(py::init<>());
    // // Electrode class
    py::class_<Electrode>(m, "Electrode")
        .def(py::init<double, double, double, double, double, double, double, double, double, double, double, double, double, double, double, double,
                      std::function<double(double)>, std::function<double(double)>>(),
             py::arg("L"), py::arg("A"), py::arg("kappa"), py::arg("epsilon"), py::arg("max_conc"), py::arg("R"), py::arg("S"),
             py::arg("T_ref"), py::arg("D_ref"), py::arg("k_ref"), py::arg("Ea_D"), py::arg("Ea_R"), py::arg("alpha"),
             py::arg("brugg"), py::arg("SOC"), py::arg("T"), py::arg("func_OCP"), py::arg("func_dOCPdT"));
    //     // getters
    //     .def_property_readonly("A", &Electrode::get_A)
    //     .def_property_readonly("S", &Electrode::get_S)
    //     .def_property_readonly("c_max", &Electrode::get_c_max)
    //     .def("R_cell", &Electrode::get_R)
    //     // properties
    //     .def_property("T", &Electrode::get_T, &Electrode::update_T)
    //     .def_property("soc", &Electrode::get_SOC, &Electrode::update_SOC)
    //     // calculations
    //     .def("ocp", &Electrode::get_OCP)
    //     .def("docpdT", &Electrode::get_dOCPdT)
    //     .def("D", &Electrode::get_D)
    //     .def("k", &Electrode::get_k)
    //     // magic methods
    //     .def("__repr__",
    //          [](const Electrode &a)
    //          {
    //              return "Electrode";
    //          });
}