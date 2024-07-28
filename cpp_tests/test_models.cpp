#include <cmath>

#include "gtest/gtest.h"

#include "models.h"

TEST(GeneralEquationsTest, CalcSOC)
{
    double actual_value = 0.027777777777777e-3;

    double cap_prev = 0.0;
    double Q = 1.5;
    double I_app = 1.5;
    double dt = 0.1;
    EXPECT_NEAR(general_equations::calc_cap(cap_prev, Q, I_app, dt), actual_value, 1e-10);
}

TEST(GeneralEquationsTest_CalcSOC_Test, Calci_0)
{
    double actual_result = 5.418867e-5;

    double k = 6.6667e-11;
    double c_s_max = 51410;
    double soc = 0.4952;
    double c_e = 1000;
    EXPECT_NEAR(general_equations::calc_i_0(k, c_s_max, soc, c_e), actual_result, 1e-10);
}

TEST(GeneralEquationsTest, CalcMolarFluxToCurrent)
{
    // positive electrode
    double actual_result = -1.656 / (96487 * 1.1167) * 96487 * 1.1167;

    double molar_flux = -1.656 / (96487 * 1.1167);
    double S = 1.1167;
    double current = general_equations::molar_flux_to_current(molar_flux, S, 'p');
    EXPECT_NEAR(current, actual_result, 1e-10);

    actual_result = -actual_result;
    current = general_equations::molar_flux_to_current(molar_flux, S, 'n');
    EXPECT_NEAR(current, actual_result, 1e-10);
}

TEST(ROMSEITest, CalJi)
{
    double actual_result = -2.193626517e-5;
    double I = 1.656;
    double j_tot = -I / (96487 * 0.7824);
    double j_s = 0.0;

    ROMSEI solver_instance = ROMSEI();
    EXPECT_EQ(solver_instance.calc_j_i(j_tot, j_s), -2.1936265167099342e-05);
}

TEST(ROMSEITest, CalcEta)
{
    double I = 1.656;
    double j_tot = -I / ((96487 * 0.7824));
    double j_s = 0.0;
    double temp = 298.15;
    double i_0 = general_equations::calc_i_0(1.764e-11, 31833, 0.7522, 1000);

    ROMSEI model_instance = ROMSEI();
    double j_i = model_instance.calc_j_i(j_tot, j_s);
    EXPECT_NEAR(j_i, -2.193626517e-5, 1e-10);

    double actual_result = (2 * (8.314) * temp / 96487) * std::asinh(j_i / (2 * i_0));
    EXPECT_NEAR(model_instance.calc_eta_n(temp, j_i, i_0), actual_result, 1e-5);
}

TEST(ROMSEITest, TestMethodCalcJs)
{
    double temp = 298.15;
    double eta_s = -0.377814;

    ROMSEI solver;

    double i_0_s = 1.14264e-5;
    EXPECT_NEAR(1.783e-2, solver.calc_j_s(temp, i_0_s, eta_s), 1e-1);

    i_0_s = 1.14264e-15;
    EXPECT_NEAR(-1.783e-12, solver.calc_j_s(temp, i_0_s, eta_s), 1e-14);
}
