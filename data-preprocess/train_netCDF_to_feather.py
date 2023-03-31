#!/usr/bin/env python
# coding: utf-8

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyarrow

data_path ='../EUPPdata/'
out_data_path='../data/'

fcs = xr.open_dataarray(f'{data_path}ESSD_benchmark_training_data_forecasts.nc')
obs = xr.open_dataarray(f'{data_path}ESSD_benchmark_training_data_observations.nc')

# ### fcs

df_fcs = fcs.to_dataframe(name = 't2m').reset_index()
df_fcs = df_fcs.dropna(axis = 0)

# ### obs

df_obs = obs.to_dataframe('t2m').reset_index()
df_obs = df_obs.dropna(axis = 0)
df_obs = df_obs.rename(columns = {'t2m':'obs'})

# takes a few minutes
df_train = pd.merge(df_obs, df_fcs,on= ['time','year','step','station_id', 'station_name'], how = 'outer')


# takes a few minutes
df_train.to_feather(f'{out_data_path}ESSD_benchmark_training_data.feather')

