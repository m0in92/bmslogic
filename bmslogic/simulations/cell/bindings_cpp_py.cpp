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

#include "calc_helpers/constants.h"
#include "general_ocps.h"
#include "battery_components.h"
#include "models.h"
#include "cyclers.h"
#include "solution.h"
#include "coords.h"
#include "solvers.h"

namespace py = pybind11;

PYBIND11_MODULE(cell, m)
{
     m.doc() = "This module contains the classes and functionalities associated with the battery cell simulations.";

     /*
      * General open circuit potential functions
      */
     m.def("LCO", py::overload_cast<double &>(&positive_electrode_ocps::LCO), py::arg("soc"));
     m.def("LCO", py::overload_cast<std::vector<double> &>(&positive_electrode_ocps::LCO), py::arg("soc"));
     m.def("NMC", py::overload_cast<double &>(&positive_electrode_ocps::NMC), py::arg("soc"));
     m.def("NMC", py::overload_cast<std::vector<double> &>(&positive_electrode_ocps::NMC), py::arg("soc"));
     m.def("LFP", py::overload_cast<double &>(&positive_electrode_ocps::LFP), py::arg("soc"));
     m.def("LFP", py::overload_cast<std::vector<double> &>(&positive_electrode_ocps::LFP), py::arg("soc"));
     m.def("LMO", py::overload_cast<double &>(&positive_electrode_ocps::LMO), py::arg("soc"));
     m.def("LMO", py::overload_cast<std::vector<double> &>(&positive_electrode_ocps::LMO), py::arg("soc"));
     m.def("NCA", py::overload_cast<double &>(&positive_electrode_ocps::NCA), py::arg("soc"));
     m.def("NCA", py::overload_cast<std::vector<double> &>(&positive_electrode_ocps::NCA), py::arg("soc"));

     m.def("graphite", py::overload_cast<double &>(&negative_electrode_ocps::graphite), py::arg("soc"));
     m.def("graphite", py::overload_cast<std::vector<double> &>(&negative_electrode_ocps::graphite), py::arg("soc"));

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
         .def(py::init<double, double, double, double, double, double, double, double, double>(),
              py::arg("conc"), py::arg("L"), py::arg("kappa"), py::arg("epsilon_n"), py::arg("epsilon"), py::arg("epsilon_p"),
              py::arg("D_e"), py::arg("t_c"), py::arg("brugg"))
         .def_property_readonly("conc", &Electrolyte::get_conc)
         .def_property_readonly("L", &Electrolyte::get_L)
         .def_property_readonly("kappa", &Electrolyte::get_kappa)
         .def_property_readonly("epsilon", &Electrolyte::get_epsilon)
         .def_property_readonly("brugg", &Electrolyte::get_brugg)
         .def_property_readonly("epsilon_p", &Electrolyte::get_epsilon_p)
         .def_property_readonly("epsilon_n", &Electrolyte::get_epsilon_n)
         .def_property_readonly("D_e", &Electrolyte::get_D_e)
         .def_property_readonly("t_c", &Electrolyte::get_t_c)
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

     // ECMBatteryCell Class
     py::class_<ECMBatteryCell>(m, "ECMBatteryCell")
         .def(py::init<double, double, double, double, double, double,
                       double, double, double, double, double, double, double, double,
                       double, double,
                       std::function<double(double)>, std::function<double(double)>, std::function<double(double)>,
                       double, double, double>(),
              py::arg("R0_ref"), py::arg("R1_ref"), py::arg("C1"), py::arg("temp_ref"), py::arg("Ea_R0"), py::arg("Ea_R1"),
              py::arg("rho"), py::arg("vol"), py::arg("c_p"), py::arg("h"), py::arg("area"), py::arg("cap"), py::arg("V_max"), py::arg("V_min"),
              py::arg("soc_init"), py::arg("temp_init"),
              py::arg("func_eta"), py::arg("func_ocv"), py::arg("func_docvdtemp"),
              py::arg("M_0"), py::arg("M"), py::arg("gamma"))
         .def_property_readonly("R0_ref", &ECMBatteryCell::get_R0_ref)
         .def_property_readonly("R1_ref", &ECMBatteryCell::get_R1_ref)
         .def_property_readonly("C1", &ECMBatteryCell::get_C1)
         .def_property_readonly("temp_ref", &ECMBatteryCell::get_temp_ref)
         .def_property_readonly("Ea_R0", &ECMBatteryCell::get_Ea_R0)
         .def_property_readonly("Ea_R1", &ECMBatteryCell::get_Ea_R1)
         .def_property_readonly("rho", &ECMBatteryCell::get_rho)
         .def_property_readonly("vol", &ECMBatteryCell::get_vol)
         .def_property_readonly("C_p", &ECMBatteryCell::get_C_p)
         .def_property_readonly("h", &ECMBatteryCell::get_h)
         .def_property_readonly("area", &ECMBatteryCell::get_area)
         .def_property_readonly("cap", &ECMBatteryCell::get_cap)
         .def_property_readonly("V_max", &ECMBatteryCell::get_V_max)
         .def_property_readonly("V_min", &ECMBatteryCell::get_V_min)
         .def_property_readonly("soc_min", &ECMBatteryCell::get_soc_min)
         .def_property_readonly("temp_init", &ECMBatteryCell::get_temp_init)
         .def_property_readonly("M0", &ECMBatteryCell::get_M0)
         .def_property_readonly("M", &ECMBatteryCell::get_M)
         .def_property_readonly("gamma", &ECMBatteryCell::get_gamma)
         .def_property_readonly("ocv", &ECMBatteryCell::get_ocv)
         // .def_property_readonly("eta", &ECMBatteryCell::get_eta)
         .def("calc_ocv", &ECMBatteryCell::calc_ocv, py::arg("soc"));

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

     // Thevenin1RC
     py::class_<Thevenin1RC>(m, "Thevenin1RC")
         .def(py::init<>())
         .def("soc_next", &Thevenin1RC::soc_next, py::arg("dt"), py::arg("i_app"), py::arg("soc_prev"), py::arg("Q"), py::arg("eta"))
         .def("i_R1_next", &Thevenin1RC::i_R1_next, py::arg("dt"), py::arg("i_app"), py::arg("i_R1_prev"), py::arg("R1"), py::arg("C1"))
         .def("V", &Thevenin1RC::V);

     // ESC
     py::class_<ESC>(m, "ESC")
         .def(py::init<>())
         .def("sign", py::overload_cast<int &>(&ESC::sign), py::arg("num"))
         .def("sign", py::overload_cast<double &>(&ESC::sign), py::arg("num"))
         .def("s", &ESC::s, py::arg("i_app"), py::arg("s_prev"))
         .def("soc_next", &ESC::soc_next, py::arg("dt"), py::arg("i_app"), py::arg("soc_prev"), py::arg("Q"), py::arg("eta"))
         .def("i_R1_next", &ESC::i_R1_next, py::arg("dt"), py::arg("i_app"), py::arg("i_R1_prev"), py::arg("R1"), py::arg("C1"))
         .def("h_next", &ESC::h_next, py::arg("dt"), py::arg("i_app"), py::arg("eta"), py::arg("gamma"), py::arg("cap"), py::arg("h_prev"))
         .def("V", &ESC::v,
              py::arg("i_app"), py::arg("ocv"),
              py::arg("R0"), py::arg("R1"), py::arg("i_R1"),
              py::arg("m_0"), py::arg("m"), py::arg("h"), py::arg("s_prev"));

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

     py::class_<ChargeRest, BaseCycler>(m, "ChargeRest")
         .def(py::init<double, double, double, double, double>(),
              py::arg("charge_current"), py::arg("V_min"), py::arg("soc_lib_max"), py::arg("soc_lib"), py::arg("rest_time"));

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

     // InterpolatedCustomCycler
     py::class_<InterpolatedCustomCycler, BaseCycler>(m, "InterpolatedCustomCycler")
         .def(py::init<std::vector<double>, std::vector<double>, double, double, double, double, double, double>(),
              py::arg("t_array"), py::arg("current_array"), py::arg("dt"),
              py::arg("V_min"), py::arg("V_max"),
              py::arg("soc_lib_min"), py::arg("soc_lib_max"), py::arg("soc_lib"))
         // properties
         .def_property("t_array", &InterpolatedCustomCycler::get_t_vector, &InterpolatedCustomCycler::set_t_vector)
         .def_property("current_array", &InterpolatedCustomCycler::get_current_vector, &InterpolatedCustomCycler::set_current_vector);
     ;

     // HPPC Cycler
     py::class_<HPPCCycler, BaseCycler>(m, "HPPCCycler")
         .def(py::init<double, double, double, int, double, double, double>(),
              py::arg("t1"), py::arg("t2"), py::arg("i_app"), py::arg("n_hppc_steps"), py::arg("V_min"), py::arg("soc_lib_min"), py::arg("soc_lib"))
         .def("get_current", &HPPCCycler::get_current, py::arg("cycling_step"), py::arg("t"));

     /*
      * Solutions
      */
     py::class_<ECMSolution>(m, "ECMSolution")
         .def(py::init<>())
         .def(py::init<std::vector<double>, std::vector<double>, std::vector<double>,
                       std::vector<double>, std::vector<double>, std::vector<double>>(),
              py::arg("t"), py::arg("I"), py::arg("V"),
              py::arg("temp"), py::arg("soc"), py::arg("i_R1"))
         .def_property("t", &ECMSolution::get_t, &ECMSolution::set_t)
         .def_property("I", &ECMSolution::get_I, &ECMSolution::set_I)
         .def_property("V", &ECMSolution::get_V, &ECMSolution::set_V)
         .def_property("temp", &ECMSolution::get_temp, &ECMSolution::set_temp)
         .def_property("soc", &ECMSolution::get_soc, &ECMSolution::set_soc)
         .def_property("i_R1", &ECMSolution::get_i_R1, &ECMSolution::set_i_R1);

     py::class_<Solution>(m, "Solution")
         .def(py::init<>())
         .def(py::init<std::vector<double>,
                       std::vector<std::string>,
                       std::vector<double>,
                       std::vector<double>,
                       std::vector<double>,
                       std::vector<double>,
                       std::vector<double>>(),
              py::arg("t"), py::arg("cycling_step"), py::arg("V"), py::arg("temp"), py::arg("cap"), py::arg("soc_p"), py::arg("soc_n"))
         .def_property("t", &Solution::get_t, &Solution::set_t)
         .def_property("cycling_step", &Solution::get_cycling_step, &Solution::set_cycling_step)
         .def_property("V", &Solution::get_V, &Solution::set_V)
         .def_property("temp", &Solution::get_temp, &Solution::set_temp)
         .def_property("cap", &Solution::get_cap, &Solution::set_cap)
         .def_property("soc_p", &Solution::get_x_p, &Solution::set_x_p)
         .def_property("soc_n", &Solution::get_x_n, &Solution::set_x_n);

     /*
      * Solvers
      */

     // ROM SEI Solver
     py::class_<ROMSEISolver>(m, "ROMSEISolver")
         .def(py::init<double, double, double, double, double,
                       double, double, double, double, double>(),
              py::arg("k"), py::arg("c_e"), py::arg("S"), py::arg("c_s_max"), py::arg("U_s"),
              py::arg("j_0_s"), py::arg("A"), py::arg("MW"), py::arg("rho"), py::arg("kappa"))
         .def_property_readonly("k", &ROMSEISolver::get_k)
         .def_property_readonly("c_e", &ROMSEISolver::get_c_e)
         .def_property_readonly("S", &ROMSEISolver::get_S)
         .def_property_readonly("c_s_max", &ROMSEISolver::get_c_s_max)
         .def_property_readonly("U_s", &ROMSEISolver::get_U_s)
         .def_property_readonly("j_0_s", &ROMSEISolver::get_j_0_s)
         .def_property_readonly("A", &ROMSEISolver::get_A)
         .def_property_readonly("MW", &ROMSEISolver::get_MW)
         .def_property_readonly("rho", &ROMSEISolver::get_rho)
         .def_property_readonly("kappa", &ROMSEISolver::get_kappa)
         .def_property_readonly("cumulative_j_s", &ROMSEISolver::get_cumulative_j_s)
         .def_property_readonly("L_SEI", &ROMSEISolver::get_L_SEI)
         .def("calc_current", &ROMSEISolver::solve_current,
              py::arg("soc"), py::arg("ocp"), py::arg("temp"), py::arg("i_app"),
              py::arg("relative_tolerance") = 1e-12, py::arg("max_iter") = 10)
         .def("calc_delta_L", &ROMSEISolver::solve_delta_L, py::arg("j_s"), py::arg("dt"))
         .def("update_L", &ROMSEISolver::update_L, py::arg("j_s"), py::arg("dt"));

     // Lumped Thermal Solver
     py::class_<LumpedThermalSolver>(m, "LumpedThermalSolver")
         .def(py::init<double, double, double, double, double, double>(),
              py::arg("h"), py::arg("A"), py::arg("rho"), py::arg("vol"), py::arg("C_p"), py::arg("temp_init"))
         // methods for calculations
         .def("reversible_heat", &LumpedThermalSolver::reversible_heat,
              py::arg("dOCPdT_p"), py::arg("dOCPdT_n"),
              py::arg("current"), py::arg("temp"))
         .def("irreversible_heat", &LumpedThermalSolver::irreversible_heat,
              py::arg("OCP_p"), py::arg("OCP_n"), py::arg("current"), py::arg("V"))
         .def("heat_transfer", &LumpedThermalSolver::heat_transfer,
              py::arg("temp"), py::arg("temp_amb"))
         .def("solve_temp", &LumpedThermalSolver::solve_temp,
              py::arg("dt"), py::arg("t_prev"), py::arg("I"), py::arg("V"),
              py::arg("temp_amb"),
              py::arg("OCP_p"), py::arg("OCP_n"), py::arg("dOCPdT_p"), py::arg("dOCPdT_n"))
         // getters
         .def("temp", &LumpedThermalSolver::get_temp)
         .def("temp_init", &LumpedThermalSolver::get_temp_init)
         .def("temp_prev", &LumpedThermalSolver::get_temp_prev);

     // Lithium Ion in Solid Electrode Solvers
     // // Eigen Solver
     py::class_<EigenSolver>(m, "EigenSolver")
         .def(py::init<char, double, int>(),
              py::arg("electrode_type"), py::arg("soc_init"), py::arg("num_roots"), py::return_value_policy::reference)
         // getters
         .def("roots", &EigenSolver::get_roots, py::return_value_policy::copy)
         .def("integ_term", &EigenSolver::get_integ_term, py::return_value_policy::copy)
         .def("vec_u_k", &EigenSolver::get_vec_u_k, py::return_value_policy::copy)
         // calculations
         .def("j_scaled", &EigenSolver::j_scaled,
              py::arg("i_app"), py::arg("R"), py::arg("S"), py::arg("D_s"), py::arg("c_s_max"))
         .def("update_integ_term", &EigenSolver::update_integ_term, py::return_value_policy::reference,
              py::arg("dt"), py::arg("i_app"), py::arg("R"), py::arg("S"), py::arg("D_s"), py::arg("c_s_max"))
         .def("du_kdt", &EigenSolver::du_kdt,
              py::arg("root"), py::arg("D"), py::arg("R"), py::arg("scaled_j_value"),
              py::arg("t"), py::arg("u"))
         .def("solve_u_k", &EigenSolver::solve_u_k,
              py::arg("root"), py::arg("t_prev"), py::arg("dt"),
              py::arg("u_k_prev"), py::arg("i_app"), py::arg("R"),
              py::arg("S"), py::arg("D_s"), py::arg("c_s_max"))
         .def("update_vec_uk", &EigenSolver::update_vec_u_k,
              py::arg("dt"), py::arg("t_prev"), py::arg("i_app"), py::arg("R"),
              py::arg("S"), py::arg("D_s"), py::arg("c_s_max"))
         .def("get_summation_term", &EigenSolver::get_summation_term,
              py::arg("dt"), py::arg("t_prev"), py::arg("i_app"), py::arg("R"),
              py::arg("S"), py::arg("D_s"), py::arg("c_s_max"))
         .def("calc_soc_surf", &EigenSolver::solve,
              py ::arg("dt"), py::arg("t_prev"), py::arg("i_app"), py::arg("R"),
              py::arg("S"), py::arg("D_s"), py::arg("c_s_max"));

     // // CN Solver
     py::class_<CNSolver>(m, "CNSolver")
         .def(py::init<double, char, int>(), py::arg("c_init"), py::arg("electrode_type"), py::arg("num_spatial_pts"))
         .def_property_readonly("K", &CNSolver::get_spatial_pts)
         .def_property_readonly("c_s_surf", &CNSolver::get_c_s_surf)
         .def("calc_A", &CNSolver::calc_A, py::arg("dt"), py::arg("R"), py::arg("D"))
         .def("calc_B", &CNSolver::calc_B, py::arg("dt"), py::arg("R"), py::arg("D"))
         .def_property_readonly("c_prev", &CNSolver::get_c_prev)
         .def_property_readonly("c_s", &CNSolver::get_c_surf)
         .def("solve", &CNSolver::solve, py::arg("dt"), py::arg("I_app"), py::arg("R"), py::arg("S"), py::arg("D"));

     // Co-ordinate Systems
     py::class_<ElectrolyteFVMCoordinates>(m, "ElectrolyteFVMCoordinates")
         .def(py::init<double, double, double, int, int, int>(),
              py::arg("L_n"), py::arg("L_sep"), py::arg("L_p"),
              py::arg("num_grid_n") = 10, py::arg("num_grid_sep") = 10, py::arg("num_grid_n") = 10)
         .def_property_readonly("L_n", &ElectrolyteFVMCoordinates::get_L_n)
         .def_property_readonly("L_sep", &ElectrolyteFVMCoordinates::get_L_sep)
         .def_property_readonly("L_p", &ElectrolyteFVMCoordinates::get_L_p)
         .def_property_readonly("dx_n", &ElectrolyteFVMCoordinates::get_dx_n)
         .def_property_readonly("dx_sep", &ElectrolyteFVMCoordinates::get_dx_sep)
         .def_property_readonly("dx_p", &ElectrolyteFVMCoordinates::get_dx_p)
         .def_property_readonly("array_x_n", &ElectrolyteFVMCoordinates::get_vector_x_n)
         .def_property_readonly("array_x_sep", &ElectrolyteFVMCoordinates::get_vector_x_sep)
         .def_property_readonly("array_x_p", &ElectrolyteFVMCoordinates::get_vector_x_p)
         .def_property_readonly("array_x", &ElectrolyteFVMCoordinates::get_vector_x)
         .def_property_readonly("array_dx", &ElectrolyteFVMCoordinates::get_vector_dx);

     // Electrolyte FVM Solver
     py::class_<ElectrolyteFVMSolver>(m, "ElectrolyteFVMSolver")
         .def(py::init<ElectrolyteFVMCoordinates, double, double,
                       double, double, double,
                       double, double,
                       double, double>(),
              py::arg("fvm_coords"), py::arg("c_e_init"), py::arg("t_c"),
              py::arg("epsilon_e_n"), py::arg("epsilon_e_sep"), py::arg("epsilon_e_p"),
              py::arg("a_s_n"), py::arg("a_s_p"),
              py::arg("D_e"), py::arg("brugg"))
         .def_property_readonly("coords", &ElectrolyteFVMSolver::get_coords)
         .def_property_readonly("t_c", &ElectrolyteFVMSolver::get_t_c)
         .def_property_readonly("c_e_init", &ElectrolyteFVMSolver::get_c_e_init)
         .def_property_readonly("epsilon_e_n", &ElectrolyteFVMSolver::get_epsilon_e_n)
         .def_property_readonly("epsilon_e_sep", &ElectrolyteFVMSolver::get_epsilon_e_sep)
         .def_property_readonly("epsilon_e_p", &ElectrolyteFVMSolver::get_epsilon_e_p)
         .def_property_readonly("a_s_n", &ElectrolyteFVMSolver::get_a_s_n)
         .def_property_readonly("a_s_p", &ElectrolyteFVMSolver::get_a_s_p)
         .def_property_readonly("D_e", &ElectrolyteFVMSolver::get_D_e)
         .def_property_readonly("brugg", &ElectrolyteFVMSolver::get_brugg)
         .def_property_readonly("array_c_e", &ElectrolyteFVMSolver::get_vector_c_e)
         .def_property_readonly("array_a_s", &ElectrolyteFVMSolver::get_vector_a_s)
         .def_property_readonly("array_D_eff", &ElectrolyteFVMSolver::get_vector_D_eff)
         .def_property_readonly("array_epsilon_e", &ElectrolyteFVMSolver::get_vector_epsilon_e)

         .def("get_calc_lower_diag", &ElectrolyteFVMSolver::get_calc_lower_diag, py::arg("dt"))
         .def("get_calc_diag", &ElectrolyteFVMSolver::get_calc_diag, py::arg("dt"))
         .def("get_calc_upper_diag", &ElectrolyteFVMSolver::get_calc_upper_diag, py::arg("dt"))
         .def("get_vec_ce_j", &ElectrolyteFVMSolver::get_vec_ce_j, py::arg("c_prev"), py::arg("j"), py::arg("dt"))

         .def("solve", &ElectrolyteFVMSolver::solve, py::arg("j"), py::arg("dt"));

     // Battery Solver
     py::class_<BatterySolver>(m, "BatterySolver")
         .def(py::init<BatteryCell, bool, bool, std::string>(),
              py::arg("battery_cell"), py::arg("is_isothermal"), py::arg("enable_degradation"),
              py::arg("electrode_mass_balance_solver") = "solver")
         .def("solve", &BatterySolver::solve, py::arg("cycler"));

     py::class_<ESPBatterySolver>(m, "ESPBatterySolver")
         .def(py::init<BatteryCell, bool, bool, std::string>(),
              py::arg("battery_cell"), py::arg("is_isothermal"), py::arg("enable_degradation"),
              py::arg("electrode_mass_balance_solver") = "solver")
         .def("solve", &ESPBatterySolver::solve, py::arg("cycler"));
}