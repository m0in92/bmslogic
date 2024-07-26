#include <vector>

#include "gtest/gtest.h"

#include "cyclers.h"

// Test BaseCycler class
TEST(BaseCyclerTest, DefaultConstructor)
{
    BaseCycler cycler;
    EXPECT_DOUBLE_EQ(cycler.get_time_elapsed(), 0.0);
    EXPECT_DOUBLE_EQ(cycler.get_V_min(), 2.5);
    EXPECT_DOUBLE_EQ(cycler.get_V_max(), 4.2);
    EXPECT_DOUBLE_EQ(cycler.get_rest_time(), 0.0);
    EXPECT_EQ(cycler.get_num_cycles(), 1);
}

TEST(BaseCyclerTest, SettersAndGetters)
{
    BaseCycler cycler;

    double V_max = 4.2;
    double rest_time = 5.0;
    int num_cycles = 100;

    cycler.set_time_elapsed(10.0);
    cycler.set_V_min(3.0);
    cycler.set_V_max(V_max);
    cycler.set_rest_time(rest_time);
    cycler.set_num_cycles(num_cycles);

    EXPECT_DOUBLE_EQ(cycler.get_time_elapsed(), 10.0);
    EXPECT_DOUBLE_EQ(cycler.get_V_min(), 3.0);
    EXPECT_DOUBLE_EQ(cycler.get_V_max(), 4.2);
    EXPECT_DOUBLE_EQ(cycler.get_rest_time(), 5.0);
    EXPECT_EQ(cycler.get_num_cycles(), 100);
}

TEST(BaseCyclerTest, ResetTimeElapsed)
{
    BaseCycler cycler;
    cycler.set_time_elapsed(10.0);
    cycler.reset_time_elapsed();
    EXPECT_DOUBLE_EQ(cycler.get_time_elapsed(), 0.0);
}

// Test Discharge class
TEST(DischargeTest, Constructor)
{
    Discharge discharge(2.0, 3.0, 20.0, 50.0);
    EXPECT_DOUBLE_EQ(discharge.discharge_current, -2.0);
    EXPECT_DOUBLE_EQ(discharge.V_min, 3.0);
    EXPECT_DOUBLE_EQ(discharge.SOC_LIB_min, 20.0);
    EXPECT_DOUBLE_EQ(discharge.SOC_LIB, 50.0);
}

// Test DischargeRest class
TEST(DischargeRestTest, Constructor)
{
    DischargeRest dischargeRest(2.0, 3.0, 20.0, 50.0, 5.0);
    EXPECT_DOUBLE_EQ(dischargeRest.discharge_current, -2.0);
    EXPECT_DOUBLE_EQ(dischargeRest.V_min, 3.0);
    EXPECT_DOUBLE_EQ(dischargeRest.SOC_LIB_min, 20.0);
    EXPECT_DOUBLE_EQ(dischargeRest.SOC_LIB, 50.0);
    EXPECT_DOUBLE_EQ(dischargeRest.rest_time, 5.0);
}

// Test Charge class
TEST(ChargeTest, Constructor)
{
    Charge charge(2.0, 4.2, 80.0, 50.0);
    EXPECT_DOUBLE_EQ(charge.charge_current, 2.0);
    EXPECT_DOUBLE_EQ(charge.V_max, 4.2);
    EXPECT_DOUBLE_EQ(charge.SOC_LIB_max, 80.0);
    EXPECT_DOUBLE_EQ(charge.SOC_LIB, 50.0);
}

TEST(CustomCyclerTest, Constructor)
{
    std::vector<double> t = {0.0, 1.0, 2.0};
    std::vector<double> current = {0.1, 0.2, 0.3};
    CustomCycler custom_cycler(t, current, 3.0, 4.2, 0.0, 1.0, 0.9);

    EXPECT_DOUBLE_EQ(custom_cycler.get_V_min(), 3.0);
    EXPECT_DOUBLE_EQ(custom_cycler.get_V_max(), 4.2);
    EXPECT_DOUBLE_EQ(custom_cycler.SOC_LIB_min, 0.0);
    EXPECT_DOUBLE_EQ(custom_cycler.SOC_LIB_max, 1.0);
    EXPECT_DOUBLE_EQ(custom_cycler.SOC_LIB, 0.9);
    EXPECT_EQ(custom_cycler.get_t_vector(), t);
    EXPECT_EQ(custom_cycler.get_current_vector(), current);
}

TEST(InterpolatedCustomCyclerTest, Constructor)
{
    std::vector<double> t_exp = {0.0, 1.0, 2.0};
    std::vector<double> I_exp = {0.1, 0.2, 0.3};
    InterpolatedCustomCycler interpCycler(t_exp, I_exp, 0.1, 3.0, 4.2, 0.0, 1.0, 0.9);

    EXPECT_DOUBLE_EQ(interpCycler.get_V_min(), 3.0);
    EXPECT_DOUBLE_EQ(interpCycler.get_V_max(), 4.2);
    EXPECT_DOUBLE_EQ(interpCycler.SOC_LIB_min, 0.0);
    EXPECT_DOUBLE_EQ(interpCycler.SOC_LIB_max, 1.0);
    EXPECT_DOUBLE_EQ(interpCycler.SOC_LIB, 0.9);
    EXPECT_EQ(interpCycler.get_t_vector().size(), 20); // Since dt=0.5, we expect 5 interpolated points
    EXPECT_EQ(interpCycler.get_current_vector().size(), 20);

    std::vector<double> t = {0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                             1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9};

    std::vector<double> I = {0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.15, 0.17, 0.18, 0.19, 0.20,
                             0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29};

    for (int idx = 0; idx < t.size(); idx++)
        EXPECT_NEAR(t[idx], interpCycler.get_t_vector()[idx], 1e-14);

    for (int idx = 0; idx < I.size(); idx++)
        EXPECT_NEAR(I[idx], interpCycler.get_current_vector()[idx], 0.1);
}
