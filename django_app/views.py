from typing import Any, Optional

from django.http import HttpResponse
from django.shortcuts import render

from bmslogic.simulations.cell.battery_components import PyECMBatteryCell
from bmslogic.simulations.cell.solution import PyECMSolution
# from bmslogic.simulations.cell.solvers import PyDTSolver

import bmslogic.simulations.cell.cell as cell_sim
from bmslogic.simulations.cell import pycyclers
from bmslogic.simulations.cell.parameter_set_manager import ParameterSets

from django_app.forms import SPSimulationVariables, ECMSimulationVariables


# class Simulator:
#     """
#     Contains the functionality to perform battery cell simulations using SPPy package.
#     """
#     available_models: list = ['SP', 'ECM']  # inherent battery models

#     def __init__(self, battery_model: str):
#         """
#         Constructor for the simulator class.
#         :param battery_model: (str) string representing the battery model.
#         """
#         if self.check_for_valid_battery_models(battery_model=battery_model):
#             self.battery_model: str = battery_model

#     @classmethod
#     def check_for_valid_battery_models(cls, battery_model: str) -> bool:
#         """
#         Raise ValueError in case the inputted battery model is not amongst the inherent battery models.
#         """
#         if battery_model not in Simulator.available_models:
#             raise ValueError('battery_model not available.')
#         else:
#             return True

#     def _get_simulation_inputs(self, request) -> Optional[tuple[str, str, float, float]]:
#         if self.battery_model == 'ECM':
#             parameter_name: str = request.POST.get('parameter_name')
#             cycler: str = request.POST.get('cycler')
#             soc_lib_init: float = float(request.POST.get('soc_lib_init'))
#             temp_amb: float = float(request.POST.get('temp_amb'))
#             return parameter_name, cycler, soc_lib_init, temp_amb
#         else:
#             return None

#     def _perform_simulation(self, request) -> cell_sim.ECMSolution:
#         # Simulation Parameters below
#         I = 1.65
#         v_min: float = 2.5  # TODO: just use battery cell min v
#         soc_min: float = 0

#         # Perform Simulation below
#         parameter_set_name, cycler, soc_lib_init, temp_amb = self._get_simulation_inputs(
#             request=request)
#         b_cell = PyECMBatteryCell.read_from_parametersets(parameter_set_name=parameter_set_name,
#                                                         soc_init=soc_lib_init,
#                                                         temp_init=temp_amb)
#         dc = cell_sim.Discharge(
#             discharge_current=I, v_min=v_min, SOC_LIB_min=soc_min, SOC_LIB=soc_lib_init)
#         solver = cell_sim.DTSolver(
#             battery_cell_instance=b_cell, isothermal=True)
#         sol = solver.solve(cycling_step=dc)
#         # sol.array_temp = sol.array_temp - Constants.T_abs
#         return sol

#     def get_simulation_results(self, request) -> Optional[tuple[Any, Any, Any, Any]]:
#         if self.battery_model == 'ECM':
#             sol: PyECMSolution = self._perform_simulation(
#                 request=request)
#             t_sim, v_sim, soc_lib, temp_sim = sol.array_t[::10].tolist(), \
#                 sol.array_V[::10].tolist(), \
#                 sol.array_soc[::10].tolist(), \
#                 sol.array_temp[::10].tolist()
#             return t_sim, v_sim, soc_lib, temp_sim
#         else:
#             return None


# def index(request) -> HttpResponse:
#     return render(request=request, template_name='index.html', context={})


# def ecm(request) -> HttpResponse:
#     t_sim, v_sim, soc_lib, temp_sim = [], [], [], []
#     if request.method == "POST":
#         form = ECMSimulationVariables(request.POST)
#         if form.is_valid():
#             t_sim, v_sim, soc_lib, temp_sim = Simulator(
#                 battery_model='ECM').get_simulation_results(request=request)
#     else:
#         form = ECMSimulationVariables()

#     return render(request=request, template_name='ecm.html', context={'form': form,
#                                                                       't_sim': t_sim,
#                                                                       'v_sim': v_sim,
#                                                                       'soc_lib': soc_lib,
#                                                                       'temp_sim': temp_sim})


def sp(request) -> HttpResponse:
    t_sim: list = []  # list of floats intended to store the time from the simulation
    v_sim: list = []  # list of floats intended to store the voltage from the simulation
    # battery surface temperature values [K] at every time-steps.
    temp_sim: list = []
    cap_sim: list = []  # battery capacity [Ahr]
    soc_p_sim: list = []  # list of floats intended to store the soc_p from the simulation
    soc_n_sim: list = []  # list of floats intended to store the soc_p from the simulation
    if request.method == "POST":
        form = SPSimulationVariables(request.POST)
        if form.is_valid():
            simulation_inputs = get_simulation_inputs(request=request)
            sol: cell_sim.Solution = perform_simulation(
                simulation_inputs=simulation_inputs)
            t_sim, v_sim, temp_sim, cap_sim, soc_p_sim, soc_n_sim = sol.t, sol.V, sol.temp, sol.cap, sol.soc_p, sol.soc_n
    else:
        form = SPSimulationVariables()

    return render(request=request, template_name='sp.html', context={'form': form,
                                                                     't_sim': t_sim,
                                                                     'v_sim': v_sim,
                                                                     'temp_sim': temp_sim,
                                                                     "cap": cap_sim,
                                                                     'soc_p_sim': soc_p_sim,
                                                                     'soc_n_sim': soc_n_sim})


def get_simulation_inputs(request) -> tuple[str, str, float]:
    parameter_name = request.POST.get('parameter_name')
    cycler = request.POST.get('cycler')
    soc_p_init = request.POST.get('soc_p_init')
    soc_n_init = request.POST.get("soc_n_init")
    return parameter_name, cycler, soc_p_init, soc_n_init


def perform_simulation(simulation_inputs: tuple[str, str, float, float]) -> cell_sim.Solution:
    """Performs the single-particle simulation using the user's input from the SPSimulationVariables forms.

    Args:
        simulation_inputs (tuple[str, str, float, float]): tuple containing the 
                                                                1. parameter_name, 
                                                                2. cycler, 
                                                                3. soc_p_init
                                                                4. soc_n_init

    Returns:
        cell_sim.Solution: Solution object that contains the simulation results.
    """
    # Operating parameters
    I: float = 1.656  # in A
    T: float = 298.15  # in K
    V_min: float = 3  # in V
    V_max: float = 4.25  # in V
    SOC_MIN: float = 0.0
    SOC_LIB: float = 0.9
    SOC_MAX: float = 1.0
    REST_TIME: float = 3600  # in s

    # Modelling parameters
    parameter_set_name: str = simulation_inputs[0]
    cycler: str = simulation_inputs[1]
    soc_p_init: float = float(simulation_inputs[2])
    soc_n_init: float = float(simulation_inputs[3])

    # Setup battery components
    battery_cell: cell_sim.BatteryCell = ParameterSets(name=parameter_set_name).generate_BatteryCell_instance(soc_n_init=soc_n_init,
                                                                                                              soc_p_init=soc_p_init,
                                                                                                              T_amb=T,
                                                                                                              R_cell=0.0028230038442483246)

    # set-up cycler
    if cycler == "discharge":
        dc: cell_sim.Discharge = cell_sim.Discharge(
            current=I, V_min=V_min, soc_lib_min=SOC_MIN, soc_lib=SOC_LIB)
    elif cycler == "discharge_rest":
        dc: cell_sim.DischargeRest = cell_sim.DischargeRest(current=I, V_min=V_min, soc_lib_min=SOC_MIN, soc_lib=SOC_LIB,
                                                            rest_time=REST_TIME)
    elif cycler == "charge":
        SOC_LIB: float = 0.0
        dc: cell_sim.DischargeRest = cell_sim.Charge(
            current=I, V_max=V_max, soc_lib_max=SOC_MIN, soc_lib=SOC_LIB)
    elif cycler == "charge-discharge":
        SOC_LIB: float = 0.0
        dc: cell_sim.ChargeDischarge = cell_sim.ChargeDischarge(charge_current=I, discharge_current=I,
                                                                V_min=V_min, V_max=V_max,
                                                                soc_min=SOC_MIN, soc_max=SOC_MAX, soc=SOC_LIB,
                                                                rest_time=REST_TIME)
    elif cycler == "HPPC":
        dc: pycyclers.HPPCCycler = pycyclers.HPPCCycler(t1=500, t2=100, i_app=1.5,
                                                        charge_or_discharge='discharge',
                                                        V_min=2.5, V_max=4.2, soc_lib_min=0.0,
                                                        soc_lib_max=1.0, soc_lib=1.0, hppc_steps=100)
    elif cycler == "DST":
        dc: pycyclers.DSTCycler = pycyclers.DSTCycler(cap_nom=battery_cell.cap(),
                                                      V_min=2.5, V_max=4.2,
                                                      soc_min=0.0, soc_max=1.0, soc=1.0, dst_step=10)

    # set-up solver
    solver: cell_sim.BatterySolver = cell_sim.BatterySolver(battery_cell=battery_cell,
                                                            is_isothermal=False,
                                                            enable_degradation=False)

    # simulate
    sol: cell_sim.Solution = solver.solve(cycler=dc)
    return sol
