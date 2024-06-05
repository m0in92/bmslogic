from bmslogic.simulations.cell.battery_components import PyECMBatteryCell
from bmslogic.simulations.cell.cyclers import PyBaseCycler
from bmslogic.simulations.cell.solution import PyECMSolution
from bmslogic.simulations.cell.models import PyThevenin1RC, PyESC
from bmslogic.simulations.cell.solvers.battery import timer


class PyECMBaseSolver:
    def __init__(self, battery_cell_instance: PyECMBatteryCell, isothermal: bool):
        if isinstance(battery_cell_instance, PyECMBatteryCell):
            self.b_cell = battery_cell_instance
        else:
            raise TypeError("ECM_obj must be an instance of Thevenin1RC class.")

        if isinstance(isothermal, bool):
            self.isothermal = isothermal
        else:
            raise TypeError("isothermal must be a boolean (True or False).")

        self.b_model = PyThevenin1RC()


class PyESCDTSolver(PyECMBaseSolver):
    def __init__(self, battery_cell_instance: PyECMBatteryCell, isothermal: bool):
        super().__init__(battery_cell_instance=battery_cell_instance,
                         isothermal=isothermal)

    @timer
    def solve_standard_cycling_step(self, cycler: PyBaseCycler, dt: float) -> PyECMSolution:
        sol = PyECMSolution()

        # Below are the intial simulation parameters
        i_R1: float = 0.0
        h: float = 0.0
        s: float = 0.0

        for cycle_no in range(cycler.num_cycles):
            for step in cycler.cycle_steps:
                t_prev: float = 0.0
                step_completed: bool = False

                while not step_completed:
                    t_curr = t_prev + dt
                    i_app: float = -cycler.get_current(step_name=step, t=t_curr)

                    # The steps below calculates the cell terminal potential
                    self.b_cell.soc = PyESC.soc_next(dt=dt, i_app=i_app, SOC_prev=self.b_cell.soc, Q=self.b_cell.cap,
                                                   eta=self.b_cell.eta)
                    i_R1_prev: float = i_R1
                    i_R1 = PyESC.i_R1_next(dt=dt, i_app=i_app, i_R1_prev=i_R1, R1=self.b_cell.R1, C1=self.b_cell.C1)
                    h_prev: float = h
                    h = PyESC.h_next(dt=dt, i_app=i_app, eta=self.b_cell.eta, gamma=self.b_cell.gamma,
                                   cap=self.b_cell.cap, h_prev=h)
                    s_prev: float = s
                    s = PyESC.s(i_app=i_app, s_prev=s)
                    v = PyESC.v(i_app=i_app, ocv=self.b_cell.ocv, R0=self.b_cell.R0, R1=self.b_cell.R1, i_R1=i_R1_prev,
                              m_0=self.b_cell.M_0, m=self.b_cell.M, h=h_prev, s_prev=s_prev)

                    # Calc temp
                    if self.isothermal is not True:
                        self.b_cell.temp = calc_cell_temp(t_prev=t_prev, dt=dt, temp_prev=self.b_cell.temp, V=v,
                                                          I=-i_app,
                                                          rho=self.b_cell.rho, Vol=self.b_cell.vol, C_p=self.b_cell.c_p,
                                                          OCV=self.b_cell.ocv, dOCVdT=self.b_cell.docpdtemp,
                                                          h=self.b_cell.h,
                                                          A=self.b_cell.area, T_amb=self.b_cell.temp_init)

                    # Loop termination criteria
                    if (step == 'charge') and (v > cycler.v_max):
                        step_completed = True
                    if (step == 'discharge') and (v < cycler.v_min):
                        step_completed = True
                    if (step == 'rest') and (t_curr > cycler.rest_time):
                        step_completed = True

                    # Below updates the simulation parameters
                    t_prev = t_curr
                    cycler.time_elapsed += dt

                    # update solution object
                    sol.update(t=cycler.time_elapsed, i_app=i_app, v=v, temp=self.b_cell.temp, soc=self.b_cell.soc, i_r1=i_R1_prev)

        return sol