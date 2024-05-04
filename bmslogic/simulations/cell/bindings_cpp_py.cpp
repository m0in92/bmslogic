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
#include "models.h"
#include "cyclers.h"

namespace py = pybind11;

PYBIND11_MODULE(cell, m)
{
     /*
      * Bindings pertaining to battery components
      */

     // Electrode class
     py::class_<Electrode>(m, "Electrode")
         .def(py::init<double, double, double, double, double, double, double, double, double, double, double, double, double, double, double, double,
                       std::function<double(double)>, std::function<double(double)>>(),
              py::arg("L"), py::arg("A"), py::arg("kappa"), py::arg("epsilon"), py::arg("max_conc"), py::arg("R"), py::arg("S"),
              py::arg("T_ref"), py::arg("D_ref"), py::arg("k_ref"), py::arg("Ea_D"), py::arg("Ea_R"), py::arg("alpha"),
              py::arg("brugg"), py::arg("SOC"), py::arg("T"), py::arg("func_OCP"), py::arg("func_dOCPdT"))
         // getters
         .def_property_readonly("A", &Electrode::get_A)
         .def_property_readonly("S", &Electrode::get_S)
         .def_property_readonly("c_max", &Electrode::get_c_max)
         .def("R_cell", &Electrode::get_R)
         // properties
         .def_property("T", &Electrode::get_T, &Electrode::update_T)
         .def_property("soc", &Electrode::get_SOC, &Electrode::update_SOC)
         // calculations
         .def("ocp", &Electrode::get_OCP)
         .def("docpdT", &Electrode::get_dOCPdT)
         .def("D", &Electrode::get_D)
         .def("k", &Electrode::get_k)
         // magic methods
         .def("__repr__",
              [](const Electrode &a)
              {
                   return "Electrode";
              });

     // PElectrode class
     py::class_<PElectrode, Electrode>(m, "PElectrode")
         .def(py::init<double, double, double, double, double, double, double, double, double, double, double, double, double, double, double, double,
                       std::function<double(double)>, std::function<double(double)>>(),
              py::arg("L"), py::arg("A"), py::arg("kappa"), py::arg("epsilon"), py::arg("max_conc"), py::arg("R"), py::arg("S"),
              py::arg("T_ref"), py::arg("D_ref"), py::arg("k_ref"), py::arg("Ea_D"), py::arg("Ea_R"), py::arg("alpha"),
              py::arg("brugg"), py::arg("SOC"), py::arg("T"), py::arg("func_OCP"), py::arg("func_dOCPdT"))
         // magic methods
         .def("__repr__", [](const PElectrode &a)
              { return "PElectrode"; });

     // NElectrode class
     py::class_<NElectrode, Electrode>(m, "NElectrode")
         .def(py::init<double, double, double, double, double, double, double, double, double, double, double, double, double, double, double, double,
                       std::function<double(double)>, std::function<double(double)>>(),
              py::arg("L"), py::arg("A"), py::arg("kappa"), py::arg("epsilon"), py::arg("max_conc"), py::arg("R"), py::arg("S"),
              py::arg("T_ref"), py::arg("D_ref"), py::arg("k_ref"), py::arg("Ea_D"), py::arg("Ea_R"), py::arg("alpha"),
              py::arg("brugg"), py::arg("SOC"), py::arg("T"), py::arg("func_OCP"), py::arg("func_dOCPdT"))
         // magic methods
         .def("__repr__", [](const NElectrode &a)
              { return "NElectrode"; });

     // Electrolyte class
     py::class_<Electrolyte>(m, "Electrolyte")
         .def(py::init<double, double, double, double, double>(),
              py::arg("conc"), py::arg("L"), py::arg("kappa"), py::arg("epsilon"), py::arg("brugg"))
         .def_property_readonly("conc", &Electrolyte::get_conc)
         .def_property_readonly("L", &Electrolyte::get_L)
         .def_property_readonly("kappa", &Electrolyte::get_kappa)
         .def_property_readonly("epsilon", &Electrolyte::get_epsilon)
         .def_property_readonly("brugg", &Electrolyte::get_brugg)
         .def("kappa_eff", &Electrolyte::get_kappa_eff);

     // BatteryCell class
     py::class_<BatteryCell>(m, "BatteryCell")
         .def(py::init<PElectrode, NElectrode, Electrolyte, double, double, double, double, double, double, double, double, double>(),
              py::arg("p_elec"), py::arg("n_elec"), py::arg("electrolyte"),
              py::arg("rho"), py::arg("Vol"), py::arg("C_p"), py::arg("h"), py::arg("A"), py::arg("cap"),
              py::arg("V_max"), py::arg("V_min"), py::arg("R_cell"))
         .def(py::init<double, double, double, double, double, double, double,
                       double, double, double, double, double, double,
                       double, double, double,
                       std::function<double(double)>, std::function<double(double)>,
                       double, double, double, double, double,
                       double, double, double, double, double, double, double,
                       double, double, double, double, double, double,
                       double, double, double,
                       std::function<double(double)>, std::function<double(double)>,
                       double, double,
                       double, double, double, double, double, double, double>(),
              py::arg("L_p"), py::arg("A_p"), py::arg("kappa_p"), py::arg("epsilon_p"), py::arg("max_conc_p"),
              py::arg("R_p"), py::arg("S_p"), py::arg("T_ref_p"), py::arg("D_ref_p"), py::arg("k_ref_p"),
              py::arg("Ea_D_p"), py::arg("Ea_R_p"), py::arg("alpha_p"), py::arg("brugg_p"), py::arg("SOC_p"),
              py::arg("T_p"),
              py::arg("func_OCP_p"), py::arg("func_dOCPdT_p"),

              py::arg("conc_e"), py::arg("L_s"), py::arg("kappa_s"), py::arg("epsilon_s"), py::arg("brugg_s"),

              py::arg("L_n"), py::arg("A_n"), py::arg("kappa_n"), py::arg("epsilon_n"),
              py::arg("max_conc_n"), py::arg("R_n"), py::arg("S_n"), py::arg("T_ref_n"),
              py::arg("D_ref_n"), py::arg("k_ref_n"), py::arg("Ea_D_n"), py::arg("Ea_R_n"),
              py::arg("alpha_n"), py::arg("brugg_n"), py::arg("SOC_n"), py::arg("T_n"),
              py::arg("func_OCP_n"), py::arg("func_dOCPdT_n"),

              py::arg("rho"), py::arg("Vol"), py::arg("C_p"), py::arg("h"), py::arg("A"), py::arg("cap"),
              py::arg("V_max"), py::arg("V_min"), py::arg("R_cell"))
         .def_property_readonly("p_elec", &BatteryCell::get_elec_p)
         .def_property_readonly("n_elec", &BatteryCell::get_elec_n)
         .def_property_readonly("electrolyte", &BatteryCell::get_electrolyte)
         .def("T", &BatteryCell::get_T)
         .def("rho", &BatteryCell::get_rho)
         .def("vol", &BatteryCell::get_Vol)
         .def("C_p", &BatteryCell::get_C_p)
         .def("h", &BatteryCell::get_h)
         .def("A", &BatteryCell::get_A)
         .def("cap", &BatteryCell::get_cap)
         .def("V_max", &BatteryCell::get_V_max)
         .def("V_min", &BatteryCell::get_V_min)
         .def_property("R_cell", &BatteryCell::get_R_cell, &BatteryCell::set_R_cell);

     /*
      * Pertaining to models
      */

     // general equations
     m.def("calc_cap", &general_equations::calc_cap,
           py::arg("cap_prev"), py::arg("Q"), py::arg("I"), py::arg("dt"));
     m.def("calc_i_0", &general_equations::calc_i_0,
           py::arg("k"), py::arg("c_s_max"), py::arg("soc"), py::arg("c_e"));
     m.def("molar_flux_to_current", &general_equations::molar_flux_to_current,
           py::arg("molar_flux"), py::arg("S"), py::arg("electrode_type"));

     // Enhanced single particle model
     m.def("ESPModel_molar_flux_electrode", &ESPModel::molar_flux_electrode, py::arg("i_app"), py::arg("S"), py::arg("electrode_type"));
     m.def("ESPModel_a_s", &ESPModel::a_s, py::arg("epsilon"), py::arg("R"));
     m.def("ESPModel_i_0", &ESPModel::i_0, py::arg("k"), py::arg("c_s_max"), py::arg("c_e"), py::arg("soc_surf"));
     m.def("ESPModel_m", &ESPModel::m,
           py::arg("i_app"), py::arg("k"), py::arg("S"), py::arg("c_s_max"), py::arg("c_e"), py::arg("soc_surf"));
     m.def("ESPModel_calc_terminal_voltage", &ESPModel::calc_terminal_voltage,
           py::arg("ocp_p"), py::arg("ocp_n"), py::arg("m_p"), py::arg("m_n"),
           py::arg("L_n"), py::arg("L_sep"), py::arg("L_p"),
           py::arg("kappa_eff_avg"), py::arg("k_f_avg"), py::arg("t_c"), py::arg("R_cell"),
           py::arg("c_e_n"), py::arg("c_e_p"),
           py::arg("temp"), py::arg("i_app"));

     // ROM SEI
     py::class_<ROMSEI>(m, "ROMSEI")
         .def(py::init<>())
         .def("calc_j_i", &ROMSEI::calc_j_i, py::arg("j_tot"), py::arg("j_s"), "Calculates the intercalation lithium molar flux density [mol/m2/s]")
         .def("calc_eta_n", &ROMSEI::calc_eta_n, py::arg("temp"), py::arg("j_i"), py::arg("i_0"))
         .def("calc_eta_s", &ROMSEI::calc_eta_s, py::arg("eta_n"), py::arg("ocp"), py::arg("ocp_s"))
         .def("calc_j_s", &ROMSEI::calc_j_s, py::arg("temp"), py::arg("i_0_s"), py::arg("eta_s"));

     /*
     * Cyclers
     */

    // Base cycler
     py::class_<BaseCycler>(m, "BaseCycler")
         .def(py::init<>())
         .def_property("time_elapsed", &BaseCycler::get_time_elapsed, &BaseCycler::set_time_elapsed)
         .def_property("V_min", &BaseCycler::get_V_min, &BaseCycler::set_V_min)
         .def_property("V_max", &BaseCycler::get_V_max, &BaseCycler::set_V_min)
         .def_property("rest_time", &BaseCycler::get_rest_time, &BaseCycler::set_rest_time)
         .def_property("num_cycles", &BaseCycler::get_num_cycles, &BaseCycler::set_num_cycles)
         // caluclation functions
         .def("get_current", &Discharge::get_current, py::arg("cycling_step"), py::arg("t"));

     // Discharge
     py::class_<Discharge, BaseCycler>(m, "Discharge")
         .def(py::init<double, double, double, double>(),
              py::arg("current"), py::arg("V_min"),
              py::arg("soc_lib_min"), py::arg("soc_lib"));

     // DischargeRest
     py::class_<DischargeRest, BaseCycler>(m, "DischargeRest")
         .def(py::init<double, double, double, double, double>(),
              py::arg("current"), py::arg("V_min"),
              py::arg("soc_lib_min"), py::arg("soc_lib"),
              py::arg("rest_time"));

     // Charge
     py::class_<Charge, BaseCycler>(m, "Charge")
         .def(py::init<double, double, double, double>(),
              py::arg("current"), py::arg("V_max"),
              py::arg("soc_lib_max"), py::arg("soc_lib"));

     // ChargeDischarge
     py::class_<ChargeDischarge, BaseCycler>(m, "ChargeDischarge")
         .def(py::init<double, double, double, double,
                       double, double, double, double>(),
              py::arg("charge_current"), py::arg("discharge_current"), py::arg("V_min"), py::arg("V_max"),
              py::arg("soc_min"), py::arg("soc_max"), py::arg("soc"), py::arg("rest_time"));

     // CustomCycler
     py::class_<CustomCycler, BaseCycler>(m, "CustomCycler")
         .def(py::init<std::vector<double>, std::vector<double>, double, double, double, double, double>(),
              py::arg("t_array"), py::arg("current_array"), py::arg("V_min"), py::arg("V_max"), py::arg("soc_lib_min"),
              py::arg("soc_lib_max"), py::arg("soc_lib"))
         // properties
         .def_property("t_array", &CustomCycler::get_t_vector, &CustomCycler::set_t_vector)
         .def_property("current_array", &CustomCycler::get_current_vector, &CustomCycler::set_current_vector);
     // calculations/helper methods
     //     .def("get_current", &CustomCycler::get_current);
}