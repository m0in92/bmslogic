#ifndef BMS_LOGIC_TIMED_SIMS_H
#define BMS_LOGIC_TIMED_SIMS_H

#include <iostream>
#include <chrono>
#include <thread>

/**
 * @brief This functions performs a function at timed periods. This is done by running a timer and performing a simulation step
 *        once the start of the interval begins.
 *        Since the timer is always running, there is no need to account for the time it take to perform that simulation step.
 *
 * @param simulation_total_duration Total simulation times in milliseconds
 * @param step_duration periodic intervals to perform a simulation in milliseconds
 */
void timed_simulation(double simulation_total_duration, long step_duration)
{
    bool simulation_end = false;
    bool perform_simulation = true;
    const std::chrono::high_resolution_clock::time_point time_simulation_start = std::chrono::high_resolution_clock::now();
    std::chrono::high_resolution_clock::time_point time_current;

    int step_index = 0;
    while (!simulation_end)
    {
        // run the simulation step
        time_current = std::chrono::high_resolution_clock::now();
        while ((std::chrono::duration_cast<std::chrono::milliseconds>(time_current - time_simulation_start).count() >= step_index * step_duration) &&
               (std::chrono::duration_cast<std::chrono::milliseconds>(time_current - time_simulation_start).count() < (step_index + 1) * step_duration + 1))
        {
            // perform the simulation JUST ONCE WITHIN THE STEP_DURATION
            if (perform_simulation)
                // perform simulation here
                std::cout << "Time: " << std::chrono::duration_cast<std::chrono::milliseconds>(time_current - time_simulation_start).count() << " ms" << std::endl;
            const long sleep_time {10};
            std::this_thread::sleep_for(std::chrono::milliseconds(sleep_time));
            perform_simulation = false;

            // sleep for the remaining time
            // std::this_thread::sleep_for(std::chrono::milliseconds(step_duration));
            time_current = std::chrono::high_resolution_clock::now();
        }

        // update the simulaiton loop variables for the next while loop
        perform_simulation = true;
        step_index = step_index + 1;

        // condition to end the timer
        time_current = std::chrono::high_resolution_clock::now();
        if (std::chrono::duration_cast<std::chrono::milliseconds>(time_current - time_simulation_start).count() >= simulation_total_duration)
        {
            std::cout << "Simulation Ended. Simulation Duration: " << std::chrono::duration_cast<std::chrono::milliseconds>(time_current - time_simulation_start).count() << " ms." << std::endl;
            simulation_end = true;
        }
    }
}

#endif // BMSLOGIC_TIMED_SIMS_h
