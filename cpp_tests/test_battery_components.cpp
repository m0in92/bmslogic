#include <gtest/gtest.h>

#include "example_parameters.cpp"
#include "battery_components.h"

class MockFunctions
{
public:
	static double OCP(double soc) { return soc * 2; }
	static double dOCPdT(double soc) { return soc * 0.1; }
};

/**
 * @brief Tests for the Electrode constructors and getters.
 *
 */
TEST(ElectrodeTest, ConstructorAndGetters)
{
	Electrode electrode(0.1, 0.2, 0.3, 0.4, 1.0, 0.5, 0.6, 300, 1e-14, 1e-6, 4000, 5000, 0.5, 1.5, 0.6, 320, MockFunctions::OCP, MockFunctions::dOCPdT);

	EXPECT_EQ(electrode.get_L(), 0.1);
	EXPECT_EQ(electrode.get_A(), 0.2);
	EXPECT_EQ(electrode.get_S(), 0.6);
	EXPECT_EQ(electrode.get_c_max(), 1.0);
	EXPECT_EQ(electrode.get_R(), 0.5);
	EXPECT_EQ(electrode.get_SOC(), 0.6);
	EXPECT_NEAR(electrode.get_OCP(), 1.2, 1);
	EXPECT_EQ(electrode.get_dOCPdT(), 0.06);
	EXPECT_EQ(electrode.get_T(), 320);
}

/**
 * @brief Tests if the Exception is raised in case of invalid SOC update. For SOC within 0 and 1 the update method should work as expected.
 *
 */
TEST(ElectrodeTest, UpdateSOC)
{
	Electrode electrode;
	EXPECT_THROW(electrode.update_SOC(1.2), InvalidSOCException);

	EXPECT_THROW(electrode.update_SOC(-0.5), InvalidSOCException);

	EXPECT_NO_THROW(electrode.update_SOC(0.5));
	EXPECT_EQ(electrode.get_SOC(), 0.5);
}

TEST(PElectrodeTest, ConstructorAndGetters)
{
	PElectrode pelectrode(0.1, 0.2, 0.3, 0.4, 1.0, 0.5, 0.6, 300, 1e-14, 1e-6, 4000, 5000, 0.5, 1.5, 0.6, 320, MockFunctions::OCP, MockFunctions::dOCPdT);
	EXPECT_EQ(pelectrode.electrode_type, 'p');
}

TEST(NElectrodeTest, ConstructorAndGetters)
{
	NElectrode nelectrode(0.1, 0.2, 0.3, 0.4, 1.0, 0.5, 0.6, 300, 1e-14, 1e-6, 4000, 5000, 0.5, 1.5, 0.6, 320, MockFunctions::OCP, MockFunctions::dOCPdT);
	EXPECT_EQ(nelectrode.electrode_type, 'n');
}

TEST(TestElectrolye_TestParams_Test, TestParams)
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

TEST(BatteryCellTest, ConstructorAndGetters)
{
	PElectrode pelectrode(0.1, 0.2, 0.3, 0.4, 1.0, 0.5, 0.6, 300, 1e-14, 1e-6, 4000, 5000, 0.5, 1.5, 0.6, 320, MockFunctions::OCP, MockFunctions::dOCPdT);
	NElectrode nelectrode(0.1, 0.2, 0.3, 0.4, 1.0, 0.5, 0.6, 300, 1e-14, 1e-6, 4000, 5000, 0.5, 1.5, 0.6, 320, MockFunctions::OCP, MockFunctions::dOCPdT);
	Electrolyte electrolyte(1.0, 0.1, 0.2, 0.3, 1.5);

	BatteryCell battery(pelectrode, nelectrode, electrolyte, 2500, 1.0, 900, 100, 0.5, 10, 4.2, 2.5, 0.01);

	EXPECT_EQ(battery.get_rho(), 2500);
	EXPECT_EQ(battery.get_Vol(), 1.0);
	EXPECT_EQ(battery.get_C_p(), 900);
	EXPECT_EQ(battery.get_h(), 100);
	EXPECT_EQ(battery.get_A(), 0.5);
	EXPECT_EQ(battery.get_cap(), 10);
	EXPECT_EQ(battery.get_V_max(), 4.2);
	EXPECT_EQ(battery.get_V_min(), 2.5);
	EXPECT_EQ(battery.get_R_cell(), 0.01);
}

TEST(ECMBatteryCellTest, ConstructorAndGetters)
{
	ECMBatteryCell ecm_battery(0.01, 0.02, 5000, 300, 4000, 5000, 2500, 1.0, 900, 100, 0.5, 10, 4.2, 2.5, 0.6, 320,
							   MockFunctions::OCP, MockFunctions::OCP, MockFunctions::dOCPdT, 0.01, 0.02, 0.03);

	EXPECT_EQ(ecm_battery.get_R0_ref(), 0.01);
	EXPECT_EQ(ecm_battery.get_R1_ref(), 0.02);
	EXPECT_EQ(ecm_battery.get_C1(), 5000);
	EXPECT_EQ(ecm_battery.get_temp_ref(), 300);
	EXPECT_EQ(ecm_battery.get_Ea_R0(), 4000);
	EXPECT_EQ(ecm_battery.get_Ea_R1(), 5000);
	EXPECT_EQ(ecm_battery.get_rho(), 2500);
	EXPECT_EQ(ecm_battery.get_vol(), 1.0);
	EXPECT_EQ(ecm_battery.get_C_p(), 900);
	EXPECT_EQ(ecm_battery.get_h(), 100);
	EXPECT_EQ(ecm_battery.get_area(), 0.5);
	EXPECT_EQ(ecm_battery.get_cap(), 10);
	EXPECT_EQ(ecm_battery.get_V_max(), 4.2);
	EXPECT_EQ(ecm_battery.get_V_min(), 2.5);
	EXPECT_EQ(ecm_battery.get_soc(), 0.6);
	EXPECT_EQ(ecm_battery.get_temp(), 320);
}