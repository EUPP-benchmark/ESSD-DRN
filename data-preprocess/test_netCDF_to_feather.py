#!/usr/bin/env python
# coding: utf-8

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyarrow

data_path ='../EUPPdata/'
out_data_path='../data/'

fcs_test = xr.open_dataarray(f'{data_path}ESSD_benchmark_test_data_forecasts.nc')
obs_test = xr.open_dataarray(f'{data_path}ESSD_benchmark_test_data_observations.nc')

# ### fcs

df_fcs_test = fcs_test.to_dataframe(name = 't2m').reset_index()

# ### obs

df_obs_test = obs_test.to_dataframe('t2m').reset_index()
df_obs_test = df_obs_test.dropna(axis = 0)
df_obs_test = df_obs_test.rename(columns = {'t2m':'obs'})


# takes a few minutes
df_test = pd.merge(df_obs_test, df_fcs_test,on= ['time','step','station_id', 'station_name'], how = 'outer')


# takes a few minutes
df_test.to_feather(f'{out_data_path}ESSD_benchmark_test_data.feather')

