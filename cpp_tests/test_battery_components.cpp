#include <gtest/gtest.h>

#include "example_parameters.cpp"
#include "battery_components.h"

TEST(TestElectroly_TestParams_Test, TestParams)
{
	double SOC_init_p = 0.4956, SOC_init_n = 0.7568;
	double T_init = 298;

	Electrolyte electrolyte1 = Electrolyte(c_init_e, L_e, kappa_e, epsilon_e, brugg_e);

	EXPECT_EQ(c_init_e, electrolyte1.get_conc());
	EXPECT_EQ(L_e, electrolyte1.get_L());
	EXPECT_EQ(kappa_e, electrolyte1.get_kappa());
	EXPECT_EQ(epsilon_e, electrolyte1.get_epsilon());
	EXPECT_EQ(brugg_e, electrolyte1.get_brugg());
	EXPECT_EQ(0.0, electrolyte1.get_D_e());
	EXPECT_EQ(0.0, electrolyte1.get_epsilon_n());
	EXPECT_EQ(0.0, electrolyte1.get_epsilon_p());
	EXPECT_EQ(0.0, electrolyte1.get_t_c());
}