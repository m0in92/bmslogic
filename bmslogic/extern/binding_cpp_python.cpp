#include "pybind11/pybind11.h"
#include "pybind11/stl.h"

#include "hummingbird.h"

namespace py = pybind11;

PYBIND11_MODULE(extern, m)
{
    m.doc() = "Contains the functionality to create and manipulate arrays and matrixes. It also has the functionality to read csv files.";

    py::class_<HB::DataFrames>(m, "DataFrames")
        .def_property_readonly("get_index", &HB::DataFrames::getIndex)
        .def_property_readonly("get_colnames", &HB::DataFrames::getColNames)
        .def_property_readonly("get_data", &HB::DataFrames::getData)
        .def("get_value", &HB::DataFrames::getValue);

    m.def("read_csv", &HB::read_csv);
}
