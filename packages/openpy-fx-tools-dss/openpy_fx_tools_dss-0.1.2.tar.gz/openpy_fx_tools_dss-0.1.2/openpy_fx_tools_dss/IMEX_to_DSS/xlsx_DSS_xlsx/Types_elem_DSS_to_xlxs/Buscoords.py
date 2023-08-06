# -*- coding: utf-8 -*-
# @Time    : 18/11/2022
# @Author  : Ing. Jorge Lara
# @Email   : jlara@iee.unsj.edu.ar
# @File    : ------------
# @Software: PyCharm
from typing import Dict, Any, Union

import pandas as pd
from numpy import ndarray
from pandas import Series, DataFrame
from pandas.core.arrays import ExtensionArray

from openpy_fx_tools_dss.helper_functions import *
from openpy_fx_tools_dss.interface_dss import dss, drt

def Buscoords_DSS(BBDD_OpenDSS: dict, DSS_elem_list: list):

    coord = dict()
    all_bus_names = dss.circuit_all_bus_names()

    for name in all_bus_names:
        coord[name] = dict()
        dss.circuit_set_active_bus(name)
        coord[name]['Y'] = dss.bus_read_y()
        coord[name]['X'] = dss.bus_read_x()

        coord[name]['Long'] = dss.bus_read_longitude()
        coord[name]['Lat'] = dss.bus_read_latitude()

    df_Buscoords_DSS = pd.DataFrame(pd.DataFrame(coord).T).reset_index().rename(columns={'index': f'Bus name'})
    if df_Buscoords_DSS.empty:
        df_Buscoords_DSS = pd.DataFrame(columns=['Bus name', 'Y', 'X', 'Long', 'Lat'])

    BBDD_OpenDSS['Buscoords'] = df_Buscoords_DSS
    DSS_elem_list.append('Buscoords')

    return BBDD_OpenDSS, DSS_elem_list


