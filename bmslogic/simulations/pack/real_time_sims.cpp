#include "real_time_sims.h"

void timed_simulation(double simulation_total_duration, long step_duration, BatterySolver solver_instance, BaseCycler cycler)
{
    bool simulation_end = false;
    bool perform_simulation = true;
    const std::chrono::high_resolution_clock::time_point time_simulation_start = std::chrono::high_resolution_clock::now();
    std::chrono::high_resolution_clock::time_point time_current;

    int step_index = 0;
    double t_prev = 0.0; // [s]
    double dt = 0.1;     // [s]
    std::pair<OverPotentials, bool> sim_results;
    double I_app{0.0};
    const int N_SIM_PER_STEP = static_cast<int>(step_duration / (1000 * dt));
    const double soc_n_init = solver_instance.m_b_cell.elec_n.get_SOC();

    while (!simulation_end)
    {
        // run the simulation step
        time_current = std::chrono::high_resolution_clock::now();
        while ((std::chrono::duration_cast<std::chrono::milliseconds>(time_current - time_simulation_start).count() >= step_index * step_duration) &&
               (std::chrono::duration_cast<std::chrono::milliseconds>(time_current - time_simulation_start).count() < (step_index + 1) * step_duration + 1))
        {
            // perform the simulation JUST ONCE WITHIN THE STEP_DURATION
            if (perform_simulation)
            {
                // perform simulation here
                for (int i = 0; i < N_SIM_PER_STEP; i++)
                {
                    t_prev += dt;
                    I_app = cycler.get_current("discharge", t_prev);
                    sim_results = solver_instance.solve_one_iteration(t_prev, dt, -1.656);
                }
                std::cout << "Real Time: " << std::chrono::duration_cast<std::chrono::milliseconds>(time_current - time_simulation_start).count() << " ms"
                          << " Sim Time " << t_prev << " s " << " I " << I_app << " A "
                          << " V: " << sim_results.first.V << " V "
                          << " SOC " << (solver_instance.m_b_cell.elec_n.get_SOC() / soc_n_init) << std::endl;
            }
            perform_simulation = false;

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

void timed_simulation(double simulation_total_duration, long step_duration, std::vector<BatterySolver> solver_instance, BaseCycler cycler)
{
    {
        bool simulation_end = false;
        bool perform_simulation = true;
        const std::chrono::high_resolution_clock::time_point time_simulation_start = std::chrono::high_resolution_clock::now();
        std::chrono::high_resolution_clock::time_point time_current;

        int step_index = 0;
        std::vector<double> t_prev(solver_instance.size(), 0.0); // [s]
        double dt = 0.1;     // [s]
        std::vector<std::pair<OverPotentials, bool>> sim_results(solver_instance.size());
        double I_app{0.0};
        const int N_SIM_PER_STEP = static_cast<int>(step_duration / (1000 * dt));
        // const double soc_n_init = solver_instance.m_b_cell.elec_n.get_SOC();

        while (!simulation_end)
        {
            // run the simulation step
            time_current = std::chrono::high_resolution_clock::now();
            while ((std::chrono::duration_cast<std::chrono::milliseconds>(time_current - time_simulation_start).count() >= step_index * step_duration) &&
                   (std::chrono::duration_cast<std::chrono::milliseconds>(time_current - time_simulation_start).count() < (step_index + 1) * step_duration + 1))
            {
                // perform the simulation JUST ONCE WITHIN THE STEP_DURATION
                if (perform_simulation)
                {
                    // perform simulation here
                    for (int idx_solver = 0; idx_solver < solver_instance.size(); idx_solver++)
                    {
                        for (int i = 0; i < N_SIM_PER_STEP; i++)
                        {
                            t_prev[idx_solver] += dt;
                            I_app = cycler.get_current("discharge", t_prev[idx_solver]);
                            sim_results[idx_solver] = solver_instance[idx_solver].solve_one_iteration(t_prev[idx_solver], dt, -1.656);
                        }
                        std::cout << "Real Time: " << std::chrono::duration_cast<std::chrono::milliseconds>(time_current - time_simulation_start).count() << " ms"
                                  << " Sim Time " << t_prev[idx_solver] << " s " << " I " << I_app << " A "
                                  << " V_" << idx_solver << ": " << sim_results[idx_solver].first.V << " V "
                                  << " SOC " << (solver_instance[idx_solver].m_b_cell.elec_n.get_SOC()) << std::endl;
                    }
                }
                perform_simulation = false;

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
}