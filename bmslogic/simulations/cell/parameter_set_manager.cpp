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

// #include "parameter_set_manager.h"
// #include "funcs.h"

// /**
//  * ParameterSet()
//  *
//  * Constructor for the ParameterSet Class
//  *
//  * Parameters:
//  *    parameterSetName_i: (std::string) the name of the desired parameter set
//  *
//  * Returns:
//  *     void
//  *
//  * */
// ParameterSet::ParameterSet(std::string parameterSetName_i)
// {
//     parameterSetName = parameterSetName_i;

//     update_directories();         // updates the private file directories.
//     extract_electrolyte_params(); // updates the electrolyte_param struct
//     update_electrode_params('p'); // updates the positive electrode struct
//     update_electrode_params('n'); // updates the negative electrode struct
//     update_battery_cell_params(); // updates the battery cell struct

//     update_OCP_funcs(); // updates the functions pertaining to SOC-OCP relationships
// }

// /**
//  * ParmeterSet
//  *
//  * Alternative constructor for the ParameterSet class.
//  *
//  * Parameters:
//  *     parameter_set_name_i: (std::string) the parameter set name.
//  *     parameter_set_dir_i: (std::string) the parameter set relative directory path to the cmake-build.
//  *
//  * Return:
//  *     void
//  *
//  * */
// ParameterSet::ParameterSet(std::string parameter_set_name_i, std::string parameter_set_dir_i)
// {
//     parameterSetName = parameter_set_name_i;
//     PARAMETER_SET_DIR = parameter_set_dir_i;

//     update_directories();         // updates the private file directories.
//     extract_electrolyte_params(); // updates the electrolyte_param struct
//     update_electrode_params('p'); // updates the positive electrode struct
//     update_electrode_params('n'); // updates the negative electrode struct
//     update_battery_cell_params(); // updates the battery cell struct

//     update_OCP_funcs(); // updates the functions pertaining to SOC-OCP relationships
// }

// /**
//  * parse_csv()
//  *
//  * Parses the csv and returns a HummingBird dataframes
//  *
//  * Parameters:
//  *     filePath: path of the csv file path.
//  *
//  *  Returns:
//  *     (HB::DataFrames) HummingBird dataframes.
//  * */
// HB::DataFrames ParameterSet::parse_csv(std::string filePath)
// {
//     return HB::read_csv(filePath).getColValues("Value");
// }

// /**
//  * update_directories()
//  *
//  * updates the private class variables that pertains to the directories.
//  *
//  * Parameters:
//  *     None
//  *
//  * Return:
//  *     None
//  *
//  * */
// void ParameterSet::update_directories()
// {
//     std::string DIR_PATH = PARAMETER_SET_DIR + parameterSetName;
//     POSITIVE_ELECTRODE_DIR = DIR_PATH + "/param_pos-electrode.csv";
//     NEGATIVE_ELECTRODE_DIR = DIR_PATH + "/param_neg-electrode.csv";
//     ELECTROLTYE_DIR = DIR_PATH + "/param_electrolyte.csv";
//     BATTERY_CELL_DIR = DIR_PATH + "/param_battery-cell.csv";
// }

// /**
//  * extract_electrolyte_params()
//  *
//  * extracts the electrolyte params from the csv file and updates the instance's electrolyte struct.
//  *
//  * Parameters:
//  *     None
//  *
//  * Return:
//  *     None
//  *
//  * */
// void ParameterSet::extract_electrolyte_params()
// {
//     HB::DataFrames df = parse_csv(ELECTROLTYE_DIR);
//     electrolyte_params.conc = std::stod(df.getValue("Value", "Conc. [mol m^-3]"));
//     electrolyte_params.L = std::stod(df.getValue("Value", "Thickness [m]"));
//     electrolyte_params.kappa = std::stod(df.getValue("Value", "Ionic Conductivity [S m^-1]"));
//     electrolyte_params.epsilon = std::stod(df.getValue("Value", "Volume Fraction"));
//     electrolyte_params.brugg = std::stod(df.getValue("Value", "Bruggerman Coefficient"));
// }

// /**
//  * update_electrode_params
//  *
//  * updates the structs containing the electrode parameters
//  *
//  * Parameters:
//  *     (char) represents the electrode type (either 'p' or 'n')
//  *
//  * Returns:
//  *     void
//  *
//  * */
// void ParameterSet::update_electrode_params(char electrode_type)
// {
//     if (electrode_type == 'p')
//     {
//         HB::DataFrames df = parse_csv(POSITIVE_ELECTRODE_DIR);

//         pos_electrode_params.L = std::stod(df.getValue("Value", "Electrode Thickness [m]"));
//         pos_electrode_params.A = std::stod(df.getValue("Value", "Electrode Area [m^2]"));
//         pos_electrode_params.kappa = std::stod(df.getValue("Value", "Ionic Conductivity [S m^-1]"));
//         pos_electrode_params.epsilon = std::stod(df.getValue("Value", "Volume Fraction"));
//         pos_electrode_params.S = std::stod(df.getValue("Value", "Electroactive Area [m^2]"));
//         pos_electrode_params.max_conc = std::stod(df.getValue("Value", "Max. Conc. [mol m^-3]"));
//         pos_electrode_params.R = std::stod(df.getValue("Value", "Radius [m]"));
//         pos_electrode_params.k_ref = std::stod(df.getValue("Value", "Reference Rate Constant [m^2.5 mol^-0.5 s^-1]"));
//         pos_electrode_params.D_ref = std::stod(df.getValue("Value", "Reference Diffusitivity [m^2 s^-1]"));
//         pos_electrode_params.Ea_R = std::stod(df.getValue("Value", "Activation Energy of Reaction [J mol^-1]"));
//         pos_electrode_params.Ea_D = std::stod(df.getValue("Value", "Activation Energy of Diffusion [J mol^-1]"));
//         pos_electrode_params.alpha = std::stod(df.getValue("Value", "Anodic Transfer Coefficient"));
//         pos_electrode_params.T_ref = std::stod(df.getValue("Value", "Reference Temperature [K]"));
//         pos_electrode_params.brugg = std::stod(df.getValue("Value", "Bruggerman Coefficient"));
//     }
//     else if (electrode_type == 'n')
//     {
//         HB::DataFrames df = parse_csv(NEGATIVE_ELECTRODE_DIR);

//         neg_electrode_params.L = std::stod(df.getValue("Value", "Electrode Thickness [m]"));
//         neg_electrode_params.A = std::stod(df.getValue("Value", "Electrode Area [m^2]"));
//         neg_electrode_params.kappa = std::stod(df.getValue("Value", "Ionic Conductivity [S m^-1]"));
//         neg_electrode_params.epsilon = std::stod(df.getValue("Value", "Volume Fraction"));
//         neg_electrode_params.S = std::stod(df.getValue("Value", "Electroactive Area [m^2]"));
//         neg_electrode_params.max_conc = std::stod(df.getValue("Value", "Max. Conc. [mol m^-3]"));
//         neg_electrode_params.R = std::stod(df.getValue("Value", "Radius [m]"));
//         neg_electrode_params.k_ref = std::stod(df.getValue("Value", "Reference Rate Constant [m^2.5 mol^-0.5 s^-1]"));
//         neg_electrode_params.D_ref = std::stod(df.getValue("Value", "Reference Diffusitivity [m^2 s^-1]"));
//         neg_electrode_params.Ea_R = std::stod(df.getValue("Value", "Activation Energy of Reaction [J mol^-1]"));
//         neg_electrode_params.Ea_D = std::stod(df.getValue("Value", "Activation Energy of Diffusion [J mol^-1]"));
//         neg_electrode_params.alpha = std::stod(df.getValue("Value", "Anodic Transfer Coefficient"));
//         neg_electrode_params.T_ref = std::stod(df.getValue("Value", "Reference Temperature [K]"));
//         neg_electrode_params.brugg = std::stod(df.getValue("Value", "Bruggerman Coefficient"));
//     }
// }

// void ParameterSet::update_OCP_funcs()
// {
//     if (parameterSetName == "test")
//     {
//         func_OCP_ref_p = test_parameter::OCP_ref_p;
//         func_OCP_ref_n = test_parameter::OCP_ref_n;
//         func_dOCPdT_p = test_parameter::dOCPdT_p;
//         func_dOCPdT_n = test_parameter::dOCPdT_n;
//     }
// }

// void ParameterSet::update_battery_cell_params()
// {
//     HB::DataFrames df = HB::read_csv(BATTERY_CELL_DIR);
//     battery_cell_params.rho = std::stod(df.getValue("Value", "Density [kg m^-3]"));
//     battery_cell_params.Vol = std::stod(df.getValue("Value", "Volume [m^3]"));
//     battery_cell_params.C_p = std::stod(df.getValue("Value", "Specific Heat [J K^-1 kg^-1]"));
//     battery_cell_params.h = std::stod(df.getValue("Value", "Heat Transfer Coefficient [J s^-1 K^-1]"));
//     battery_cell_params.A = std::stod(df.getValue("Value", "Surface Area [m^2]"));
//     battery_cell_params.cap = std::stod(df.getValue("Value", "Capacity [A hr]"));
//     battery_cell_params.V_max = std::stod(df.getValue("Value", "Maximum Potential Cut-off [V]"));
//     battery_cell_params.V_min = std::stod(df.getValue("Value", "Minimum Potential Cut-off [V]"));
// }
