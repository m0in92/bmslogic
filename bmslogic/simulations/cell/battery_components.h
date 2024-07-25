/**
 * @file battery_components.h
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief Contains the classes and functionalities pertaining to the storage of battery parameters.
 * @version 0.1
 * @date 2024-05-03
 *
 * @copyright Copyright (c) 2024
 *
 */

#ifndef BMSLOGIC_CELL_BATTERY_COMPONENTS_H
#define BMSLOGIC_CELL_BATTERY_COMPONENTS_H

#include <string>
#include <cmath>
#include <functional>

class InvalidSOCException : public std::exception
{
public:
    char *what()
    {
        return "SOC is beyond 0 or 1.";
    }
};

class Electrode
{
public:
    Electrode() = default;
    Electrode(double L_i, double A_i, double kappa_i, double epsilon_i, double max_conc_i, double R_i, double S_i,
              double T_ref_i, double D_ref_i, double k_ref_i, double Ea_D_i, double Ea_R_i, double alpha_i,
              double brugg_i, double SOC_i, double T_i, std::function<double(double)> func_OCP_i, std::function<double(double)> func_dOCPdT_i);
    virtual ~Electrode() = default;
    // Accessor functions
    double get_L() const { return L; }
    double get_A() const { return A; }
    double get_T() const { return T; } // returns the electrode temperature [K]
    double get_SOC() const { return SOC; }
    double get_OCP() { return calc_OCP(); }                // returns the OCP value at the inputted SOC.
    double get_dOCPdT() const { return func_dOCPdT(SOC); } // returns the dOCP/dT value at the inputted SOC.
    double get_D() { return calc_D(); }                    // calculates and returns the electrode diffusivity [m2/s]
    double get_k() { return calc_k(); }
    double get_S() const { return S; }
    double get_c_max() const { return max_conc; }
    double get_R() const { return R; }
    // Modifier functions
    void update_T(double &T_new) { T = T_new; } // updates the electrode temp.
    void update_SOC(double SOC_new)
    {
        if ((SOC < 0) || (SOC > 1))
        {
            throw InvalidSOCException();
        }
        SOC = SOC_new;
    } // update the electrode SOC
    double calc_OCP(double i_soc) { return func_OCP(i_soc); }

protected:
    double L;        // Electrode Thickness [m]
    double A;        // Electrode Area [m^2]
    double kappa;    // Ionic Conductivity [S m^-1]
    double epsilon;  // Volume Fraction
    double max_conc; // Max. Conc. [mol m^-3]
    double R;        // Radius [m]
    double S;        // Electro-active Area [m2]
    double T_ref;    // Reference Temperature [K]
    double D_ref;    // Reference Diffusivity [m2/s]
    double k_ref;    // Reference Rate Constant [m2.5 / (mol0.5 s)
    double Ea_D;     // Activation Energy of Diffusion [J / mol]
    double Ea_R;     // Activation Energy of Reaction [J / mol]
    double alpha;    // Anodic Transfer Coefficient
    double brugg;    // Bruggerman Coefficient
    double SOC_init; // initial SOC
    double SOC;      // electrode SOC
    double T;        // electrode temperature [K]

    std::function<double(double)> func_OCP;    // electrode SOC-OCP relationship at the reference temperature.
    std::function<double(double)> func_dOCPdT; // this function represents the change in OCP with temp.

    // Helper functions
    double calc_OCP();
    double calc_D();
    double calc_k();
};

class PElectrode : public Electrode
{
public:
    PElectrode() = default;
    PElectrode(double L_i, double A_i, double kappa_i, double epsilon_i, double max_conc_i, double R_i, double S_i,
               double T_ref_i, double D_ref_i, double k_ref_i, double Ea_D_i, double Ea_R_i, double alpha_i,
               double brugg_i, double SOC_i, double T_i,
               std::function<double(double)> func_OCP_i, std::function<double(double)> func_dOCPdT_i);
    ~PElectrode() = default;
    // Public attributes
    char electrode_type = 'p';
};

class NElectrode : public Electrode
{
public:
    NElectrode() = default;
    NElectrode(double L_i, double A_i, double kappa_i, double epsilon_i, double max_conc_i, double R_i, double S_i,
               double T_ref_i, double D_ref_i, double k_ref_i, double Ea_D_i, double Ea_R_i, double alpha_i,
               double brugg_i, double SOC_i, double T_i,
               std::function<double(double)> func_OCP_i, std::function<double(double)> func_dOCPdT_i);
    ~NElectrode() = default;
    // Public attributes
    char electrode_type = 'n';
};

class Electrolyte
{
public:
    Electrolyte() = default;
    Electrolyte(double conc_i, double L_i, double kappa_i, double epsilon_i, double brugg_i);
    Electrolyte(double conc_i, double L_i, double kappa_i, double i_epsilon_n, double epsilon_i, double i_epsilon_p,
                double i_D_e, double i_t_c, double brugg_i);
    ~Electrolyte() = default;
    // Accessor functions
    double get_conc() const { return conc; }
    double get_L() const { return L; }
    double get_kappa() const { return kappa; }
    double get_epsilon() const { return epsilon; }
    double get_brugg() const { return brugg; }
    double get_kappa_eff() { return kappa * std::pow(epsilon, brugg); }
    // // optional electrolyte parameters below
    double get_epsilon_p() const { return epsilon_p; }
    double get_epsilon_n() const { return epsilon_n; }
    double get_D_e() const { return D_e; }
    double get_t_c() const { return t_c; }

private:
    double conc;           // electrolyte conc. [mol/m3]
    double L;              // seperator thickness [m]
    double kappa;          // electrolyte conductivity [S/m]
    double epsilon;        // electrolyte volume fraction in the seperator region
    double epsilon_n{0.0}; // electrolyte volume fraction in the negative electrode region
    double epsilon_p{0.0}; // electrolyte volume fraction in the positive electrode region
    double D_e{0.0};       // electrolyte diffusivity [m2/s]
    double t_c{0.0};       // electrolyte cationic transference number
    double brugg;          // Bruggerman coefficient for the electrolyte
};

class BatteryCell
{
public:
    BatteryCell(PElectrode i_elec_p, NElectrode i_elec_n, Electrolyte i_electrolyte, double i_rho, double i_Vol,
                double i_C_p, double i_h, double i_A, double i_cap, double i_V_max, double i_V_min, double i_R_cell);
    BatteryCell(double L_p, double A_p, double kappa_p, double epsilon_p, double max_conc_p, double R_p, double S_p,
                double T_ref_p, double D_ref_p, double k_ref_p, double Ea_D_p, double Ea_R_p, double alpha_p,
                double brugg_p, double SOC_p, double T_p, std::function<double(double)> func_OCP_p, std::function<double(double)> func_dOCPdT_p,
                double c_e, double L_s, double kappa_s, double epsilon_s, double brugg_s,
                double L_n, double A_n, double kappa_n, double epsilon_n, double max_conc_n, double R_n, double S_n,
                double T_ref_n, double D_ref_n, double k_ref_n, double Ea_D_n, double Ea_R_n, double alpha_n,
                double brugg_n, double SOC_n, double T_n,
                std::function<double(double)> func_OCP_n, std::function<double(double)> func_dOCPdT_n,
                double i_rho, double i_Vol,
                double i_C_p, double i_h, double i_A, double i_cap, double i_V_max, double i_V_min, double i_R_cell);
    // public variables
    PElectrode elec_p;
    NElectrode elec_n;
    Electrolyte electrolyte;
    // Getter methods
    double get_T() const { return T; }
    double get_rho() const { return rho; }
    double get_Vol() const { return Vol; }
    double get_C_p() const { return C_p; }
    double get_h() const { return h; }
    double get_A() const { return A; }
    double get_cap() const { return cap; }
    double get_V_max() const { return V_max; }
    double get_V_min() const { return V_min; }
    double get_R_cell() const { return R_cell; }
    PElectrode get_elec_p() const { return elec_p; }
    NElectrode get_elec_n() const { return elec_n; }
    Electrolyte get_electrolyte() const { return electrolyte; }
    // Setter methods
    void set_R_cell(double &R_cell_new) { R_cell = R_cell_new; }
    void set_temp(double &temp_new) { T = temp_new; }

private:
    double T;      // battery cell temperature, K
    double rho;    // battery density (mostly for thermal modelling), kg/m3
    double Vol;    // battery cell volume, m3
    double C_p;    // specific heat capacity, J / (K kg)
    double h;      // heat transfer coefficient, J / (S K)
    double A;      // surface area, m2
    double cap;    // capacity, Ah
    double V_max;  // maximum potential
    double V_min;  // minimum potential
    double R_cell; // battery cell internal resistance [ohms]
};

/**
 * @brief class to store the variables for the equivalent circuit model (ECM) simulations.
 *
 */
class ECMBatteryCell
{
public:
    ECMBatteryCell(double i_R0_ref, double i_R1_ref, double i_C1, double i_temp_ref, double i_Ea_R0, double i_Ea_R1,
                   double i_rho, double i_vol, double i_c_p, double i_h, double i_area, double i_cap, double i_V_max, double i_V_min,
                   double i_soc_init, double i_temp_init,
                   std::function<double(double)> i_func_eta, std::function<double(double)> i_func_ocv, std::function<double(double)> i_func_docvdtemp,
                   double i_M_0, double i_M, double i_gamma);

    // getters
    double get_R0_ref() const { return m_R0_ref; }
    double get_R0() { return calc_R0(); }
    double get_R1_ref() const { return m_R1_ref; }
    double get_R1() { return calc_R1(); }
    double get_C1() const { return m_C1; }
    double get_temp_ref() const { return m_temp_ref; }
    double get_Ea_R0() const { return m_Ea_R0; }
    double get_Ea_R1() const { return m_Ea_R1; }
    double get_rho() const { return m_rho; }
    double get_vol() const { return m_vol; }
    double get_C_p() const { return m_c_p; }
    double get_h() const { return m_h; }
    double get_area() const { return m_area; }
    double get_cap() const { return m_cap; }
    double get_V_max() const { return m_v_max; }
    double get_V_min() const { return m_v_min; }
    double get_soc_min() const { return m_soc_init; }
    double get_temp_init() const { return m_temp_init; }
    double get_eta(double i_soc) const { return m_func_eta(i_soc); }
    double get_M0() const { return m_M_0; }
    double get_M() const { return m_M; }
    double get_gamma() const { return m_gamma; }
    double get_eta() { return m_func_eta(m_soc); }
    double get_ocv() { return calc_ocv(m_soc); }

    double get_soc() { return m_soc; }
    double get_temp() { return m_temp; }

    // setters
    void set_soc(double i_soc) { m_soc = i_soc; }

    // functions for calculations
    double calc_ocv(double i_soc) const { return m_func_ocv(i_soc) + m_func_docvdtemp(i_soc) * (m_temp - m_temp_ref); }
    double calc_R0();
    double calc_R1();

private:
    double m_R0_ref;   // resistance value of R0 [ohm]
    double m_R1_ref;   // resistance value of R1 [ohm]
    double m_C1;       // capacitance of capacitor in RC circuit [ohm]
    double m_temp_ref; // reference temperature for R0_ref and R1_ref
    double m_Ea_R0;    // activation energy for R0 [J/mol]
    double m_Ea_R1;    // activation energy for R1 [J/mol]

    double m_rho;   // battery density (mostly for thermal modelling), kg/m3
    double m_vol;   // battery cell volume, m3
    double m_c_p;   // specific heat capacity, J / (K kg)
    double m_h;     // # heat transfer coefficient, J / (S K)
    double m_area;  // surface area, m2
    double m_cap;   // capacity, Ah
    double m_v_max; // maximum potential
    double m_v_min; // minimum potential

    double m_soc_init;  // initial SOC
    double m_temp_init; // initial battery cell temperature [K]
    double m_soc;
    double m_temp; // Battery cell temperature [K]

    std::function<double(double)> m_func_eta; // func for the Columbic efficiency as a func of SOC and temp
    std::function<double(double)> m_func_ocv; // func which outputs the battery OCV from its SOC function which outputs the change of OCV with respect to temperature from its SOC
    std::function<double(double)> m_func_docvdtemp;

    // The parameters below relate the dynamic and instantaneous hysteresis
    // The instantaneous hysteresis co-efficient [V]
    double m_M_0;
    double m_M;     // SOC-dependent hysteresis co-efficient [V]
    double m_gamma; // Hysteresis time-constant
};

#endif // BMSLOGIC_CELL_BATTERY_COMPONENTS_H
