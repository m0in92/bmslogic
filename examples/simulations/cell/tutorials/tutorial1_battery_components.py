import SPCPPY as sp
from examples.example_parameter import *

if __name__ == "__main__":
    SOC_init_p: float = 0.4952
    SOC_init_n: float = 0.7522
    R_cell: float = 0.0028230038442483246
    T_amb: float = 298.15

    # The battery cell can be initiatied using the pre-loaded parameter sets.
    # To load a battery_cell instance using the parameter sets, use the "generate_BatteryCell_instance" method.
    battery_cell: sp.BatteryCell = sp.ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
                                                                                               soc_p_init=SOC_init_p,
                                                                                               T_amb=T_amb,
                                                                                               R_cell=R_cell)
    
    # The battery cell contains attributes and methods to access various battery cell parameters. For instance, the following
    # battery cell parameters can be accessed. 
    print("------------ Battery Cell's Parameters --------------")
    print(battery_cell.A()) 
    print(battery_cell.C_p())
    print(battery_cell.R_cell)
    print(battery_cell.T())
    print(battery_cell.V_max())
    print(battery_cell.V_min())

    # Furthermore, battery_cell contains electrode and electrolyte objects. An example on the access of the positive electrode's
    # attributes and methods are 
    print("------------ Positive Electrode Parameters --------------")
    print(battery_cell.p_elec.D())    # positive electrode diffusivity [m/s2] (note it is a function of temperature)
    print(battery_cell.p_elec.T)      # positive electrode temperature [K]
    print(battery_cell.p_elec.soc)    # positive electrode soc
    print(battery_cell.p_elec.A)      # positive electrode cross-sectional area [m2]
    print(battery_cell.p_elec.S)      # positive electrode electrochemically active area [m2]
    print(battery_cell.p_elec.c_max)  # positive electrode max lithium conc. [mol/m3]
    # Similarly for the negative electrode within the battery_cell instance.
    print("------------ Negative Electrode Parameters --------------")
    print(battery_cell.n_elec.D())    # positive electrode diffusivity [m/s2] (note it is a function of temperature)
    print(battery_cell.n_elec.T)      # positive electrode temperature [K]
    print(battery_cell.n_elec.soc)    # positive electrode soc
    # and again for the electrolyte
    print("------------ Electrolyte Parameters --------------")
    print(battery_cell.electrolyte.conc)        # electrolyte concentration [mol/m3] 
    print(battery_cell.electrolyte.L)           # seperator thickness m
    print(battery_cell.electrolyte.kappa)       # electrolyte ionic conductivity [S/m]
    print(battery_cell.electrolyte.epsilon)     # electrolyte volume fraction in the seperator region
    print(battery_cell.electrolyte.kappa_eff())   # effective electrolyte conductivity [S/m] 

    # Alternatively, the battery cell instance can also be constructed from the electrode and electrolyte objects. This construction is
    # useful if the parameters are not in the existing parameter sets. Such a battery cell instance can be constructed as illustrated below:
    SOC_init_p: float = 0.4952
    SOC_init_n: float = 0.7522

    p_electrode: sp.PElectrode = sp.PElectrode(L=L_p, A=A_p, kappa=kappa_p, epsilon=epsilon_p, max_conc=max_conc_p, R=R_p, S=S_p,
                                               T_ref=T_ref_p, D_ref=D_ref_p, k_ref=k_ref_p, Ea_D=Ea_D_p, Ea_R=Ea_R_p, alpha=alpha_p,
                                               brugg=brugg_p, SOC=SOC_init_p, T=T, func_OCP=OCP_ref_p, func_dOCPdT=dOCPdT_p)
    n_electrode: sp.NElectrode = sp.NElectrode(L=L_n, A=A_n, kappa=kappa_n, epsilon=epsilon_n, max_conc=max_conc_n, R=R_n, S=S_n, 
                                               T_ref=T_ref_n, D_ref=D_ref_n, k_ref=k_ref_n, Ea_D=Ea_D_n, Ea_R=Ea_R_n, alpha=alpha_n,
                                               brugg=brugg_n, SOC=SOC_init_n, T=T, func_OCP=OCP_ref_n, func_dOCPdT=dOCPdT_n)
    electrolyte: sp.Electrolyte = sp.Electrolyte(L=L_e, conc=c_init_e, kappa=kappa_e, epsilon=epsilon_e, brugg=brugg_e)
    battery_cell: sp.BatteryCell = sp.BatteryCell(p_elec=p_electrode, n_elec=n_electrode, electrolyte=electrolyte,
                                                  rho=rho, Vol=Vol, C_p=C_p, h=h, A=A, cap=cap, V_max=V_max, V_min=V_min, R_cell=R_cell)
    # this battery instance can be used just as mentioned above.
    print("------------ Battery Cell's Valid List of Attributes --------------")
    print(dir(battery_cell))