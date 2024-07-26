#include "gtest/gtest.h"

#include "cyclers.h"


// Test BaseCycler class
TEST(BaseCyclerTest, DefaultConstructor) {
    BaseCycler cycler;
    EXPECT_DOUBLE_EQ(cycler.get_time_elapsed(), 0.0);
    EXPECT_DOUBLE_EQ(cycler.get_V_min(), 2.5);
    EXPECT_DOUBLE_EQ(cycler.get_V_max(), 4.2);
    EXPECT_DOUBLE_EQ(cycler.get_rest_time(), 0.0);
    EXPECT_EQ(cycler.get_num_cycles(), 1);
}

TEST(BaseCyclerTest, SettersAndGetters) {
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

TEST(BaseCyclerTest, ResetTimeElapsed) {
    BaseCycler cycler;
    cycler.set_time_elapsed(10.0);
    cycler.reset_time_elapsed();
    EXPECT_DOUBLE_EQ(cycler.get_time_elapsed(), 0.0);
}
