"""
This module contains the forms (inherited from Django's Forms) to be used for the django apps.
"""
__all__ = ['ECMSimulationVariables', 'SPSimulationVariables']

__authors__ = "Moin Ahmed"
__copyright__ = "Copyright 2023 by SPPy. All Rights Reserved."


from django import forms

from bmslogic.simulations.cell.parameter_set_manager import ParameterSets, ECMParameterSets



class BaseBatteryModelForm(forms.Form):
    """Contains the forms choices for most, if not all, phenomenlogical and physics-based models.

    Parameters
    ----------
    forms : 
        Django's forms
    """
    lst_cycler: list = [('discharge', 'discharge'),
                        ('discharge_rest', 'discharge_rest'),
                        ('charge', 'charge'),
                        ('charge-discharge', 'charge-discharge'),
                        ('HPPC', 'HPPC'),
                        ('DST', 'DST')]
    

class ECMSimulationVariables(BaseBatteryModelForm):
    """
    Contains the field ECM simulation's user inputs.
    """
    lst_parameter_name: list = [(param_set_name, param_set_name)
                                for param_set_name in ECMParameterSets.lst_parameter_names()]
    # lst_cycler: list = [('discharge', 'discharge')]

    parameter_name = forms.ChoiceField(label="Parameter Name", choices=lst_parameter_name)
    cycler = forms.ChoiceField(choices=BaseBatteryModelForm.lst_cycler)
    soc_lib_init = forms.FloatField(label='Initial LIB SOC', min_value=-0.1, max_value=1.1)
    temp_amb = forms.FloatField(label='Ambient Temperature [K]')


class SPSimulationVariables(forms.Form):
    """    Contains the relevant fields required from the user to perform the single particle model simulations.

    These Forms include the user inputs pertaining to:
        1. parameter_set name
        2. cycler
        3. soc_p_init
        4. soc_n_init

    First the availble parameter sets are searched for and then the user input forms are created.

    Args:
        forms (_type_): Django's Form class
    """
    # Search for the availble parameter sets names.
    lst_parameter_name: list = [(param_set_name, param_set_name)
                                for param_set_name in ParameterSets.list_parameters_sets()]

    # Django's form creation below
    parameter_name = forms.ChoiceField(label="Parameter Name", choices=lst_parameter_name)
    cycler = forms.ChoiceField(choices=BaseBatteryModelForm.lst_cycler)
    soc_p_init = forms.FloatField(label='Initial Positve Electrode SOC: ', min_value=-0.1, max_value=1.1)
    soc_n_init = forms.FloatField(label='Initial Negative Electrode SOC: ', min_value=-0.1, max_value=1.1)


class SPeSimulationVariables(forms.Form):
    pass


class P2DSimulationVariables(forms.Form):
    pass