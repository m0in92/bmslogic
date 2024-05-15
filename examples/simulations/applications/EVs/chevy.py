"""
Example of using the EV simulation using the vehicle parameters from the EV dataset.
"""
__all__ = []

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."
__status__ = "Deployed"

import os
import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parent.parent.parent.parent.parent.__str__())
import bmslogic.simulations.applications as EV_sim


alias_name = "Volt_2017"
volt = EV_sim.EVFromDatabase(alias_name=alias_name)
udds = EV_sim.EVDriveCycle(drive_cycle_name="nycc")
waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
model = EV_sim.EVDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
sol = model.simulate()

# plot
sol.plot()