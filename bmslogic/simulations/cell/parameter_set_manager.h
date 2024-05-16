// /**
//  * @file parameter_set_manager.h
//  * @author Moin Ahmed (moinahmed100@gmail.com)
//  * @brief Contains the functionality to read the battery cell parameters from the csv files.
//  * @version 0.1
//  * @date 2024-05-15
//  * 
//  * @copyright Copyright (c) 2024
//  * 
//  */

// #ifndef BMSLOGIC_PARAMETER_SET_MANAGER_H
// #define BMSLOGIC_PARAMETER_SET_MANAGER_H

// #include <string>
// #include <vector>

// #include "extern/hummingbird.h"

// class ParameterSet {
// public:
//     ParameterSet(std::string);
//     ParameterSet(std::string, std::string);
//     ~ParameterSet() {};  // Destructor is an empty function since no complicated memory allocation utilized.

//     // Accessor Functions
//     std::string get_parameter_set_name() {return parameterSetName;}
//     std::string get_positive_electrode_dir() {return POSITIVE_ELECTRODE_DIR;}
//     std::string get_negative_electrode_dir() {return NEGATIVE_ELECTRODE_DIR;}
//     std::string get_electrolyte_dir() {return ELECTROLTYE_DIR;}
//     std::string get_battery_cell_dir() {return BATTERY_CELL_DIR;}
//     double get_OCP_p(double SOC) {return func_OCP_ref_p(SOC);}  // returns the OCP value at the inputted SOC.
//     double get_OCP_n(double SOC) {return func_OCP_ref_n(SOC);}  // returns the OCP value at the inputted SOC.
//     double get_dOCPdT_p(double SOC) {return func_dOCPdT_p(SOC);} // returns the dOCP/dT value at the inputted SOC.
//     double get_dOCPdT_n(double SOC) {return func_dOCPdT_n(SOC);}  // returns the dOCP/dT value at the inputted SOC.
//     auto get_func_OCP_p() {return func_OCP_ref_p;}
//     auto get_func_dOCPdT_p() {return func_dOCPdT_p;}
//     auto get_func_OCP_n() {return func_OCP_ref_n;}
//     auto get_func_dOCPdT_n() {return func_dOCPdT_n;}

//     auto& get_pos_electrode_params() {return pos_electrode_params;}
//     auto& get_neg_electrode_params() {return neg_electrode_params;}
//     auto& get_electrolyte_params() {return electrolyte_params;}
//     auto& get_battery_cell_params() {return battery_cell_params;}

//     // Helper Functions

// private:
//     std::string parameterSetName;

//     std::string PARAMETER_SET_DIR = "../../../parameter_sets/";  // file path relative to the cmake-build directory.
//     std::string POSITIVE_ELECTRODE_DIR;  // file path to the csv containing the positive electrode parameters.
//     std::string NEGATIVE_ELECTRODE_DIR;  // file path to the csv containing the negative electrode parameters.
//     std::string ELECTROLTYE_DIR;  // file path to the csv containing electrolyte parameters.
//     std::string BATTERY_CELL_DIR;  // file path to the csv containing battery cell parameters.

//     struct
//     {
//         double L; // Electrode Thickness [m]
//         double A; // Electrode Area [m^2]
//         double kappa; // Ionic Conductivity [S m^-1]
//         double epsilon; // Volume Fraction
//         double max_conc; // Max. Conc. [mol m^-3]
//         double R; // Radius [m]
//         double S; // Electroactive Area [m2]
//         double T_ref; // Reference Temperature [K]
//         double D_ref; // Reference Diffusitivity [m2/s]
//         double k_ref; // Reference Rate Constant [m2.5 / (mol0.5 s)
//         double Ea_D; // Activation Energy of Diffusion [J / mol]
//         double Ea_R; // Activation Energy of Reaction [J / mol]
//         double alpha;  // Anodic Transfer Coefficient
//         double brugg; // Bruggerman Coefficient
//     } pos_electrode_params, neg_electrode_params;

//     struct
//     {
//         double conc;  // electrolyte init conc [mol/m3]
//         double L;  // electrolyte thickness [m]
//         double kappa;  // electrolyte ionic conductivity [S/m]
//         double epsilon;  // electrolyte volume fraction
//         double brugg; // Bruggerman coefficient value for the electrolyte
//     } electrolyte_params;

//     struct
//     {
//         double rho;  // battery density (mostly for thermal modelling), kg/m3
//         double Vol;  // battery cell volume, m3
//         double C_p;  // specific heat capacity, J / (K kg)
//         double h;  // heat transfer coefficient, J / (S K)
//         double A;  // surface area, m2
//         double cap;  // capacity, Ah
//         double V_max;  // maximum potential
//         double V_min;  // minimum potential
//     } battery_cell_params;

//     double (*func_OCP_ref_p)(double);  // function representing the OCP of the positive electrode
//     double (*func_OCP_ref_n)(double);  // function representing the OCP of the positive electrode
//     double (*func_dOCPdT_p)(double);  // function representing the relationship between SOC and dOCPdT for the positive electrode.
//     double (*func_dOCPdT_n)(double);  // function representing the relationship between SOC and dOCPdT for the negative electrode.

//     // Helper funcs
//     HB::DataFrames parse_csv(std::string);
//     void update_directories();
//     void update_electrode_params(char);
//     void extract_electrolyte_params();
//     void update_OCP_funcs();
//     void update_battery_cell_params();
// };

// #endif //BMSLOGIC_PARAMETER_SET_MANAGER_H
