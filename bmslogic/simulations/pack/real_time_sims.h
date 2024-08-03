#ifndef BMS_LOGIC_TIMED_SIMS_H
#define BMS_LOGIC_TIMED_SIMS_H

#include <iostream>
#include <chrono>
#include <thread>

#include "solvers.h"

/**
 * @brief This functions performs a function at timed periods. This is done by running a timer and performing a simulation step
 *        once the start of the interval begins.
 *        Since the timer is always running, there is no need to account for the time it take to perform that simulation step.
 *
 * @param simulation_total_duration Total simulation times in milliseconds
 * @param step_duration periodic intervals to perform a simulation in milliseconds
 */
void timed_simulation(double simulation_total_duration, long step_duration, BatterySolver solver_instance, BaseCycler cycler);

#endif // BMSLOGIC_TIMED_SIMS_h
