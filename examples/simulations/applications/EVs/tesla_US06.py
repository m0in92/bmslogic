import sys

import path_definations

sys.path.append(path_definations.ROOT_DIR)

import pandas as pd

import bmslogic.simulations.applications as EV_sim


alias_name = "Tesla_2022_Model3_RWD"
tesla = EV_sim.EVFromDatabase(alias_name=alias_name)
udds = EV_sim.EVDriveCycle(drive_cycle_name="us06")
std_condition = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
model = EV_sim.EVDynamics(ev_obj=tesla, drive_cycle_obj=udds, external_condition_obj=std_condition)
sol = model.simulate()

# plot
sol.plot()