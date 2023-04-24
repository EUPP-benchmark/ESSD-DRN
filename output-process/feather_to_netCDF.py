#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data_path = '../data-feather'
orig_data_path = '../EUPPdata'
out_path = '../data-nc/'


# In[2]:


preds = pd.read_feather(f'{data_path}/fcst_all_leadtime.feather')



# In[3]:


preds_columns = list(preds.columns.drop('t2m'))
preds_ = preds.set_index(preds_columns)


# In[4]:


# takes a few minutes
da_preds = preds_.to_xarray().t2m.astype('float32')


# In[5]:


da_preds.coords


# In[6]:


da_preds.dtype


# In[7]:


# add global attributes:
da_preds.attrs['institution'] = 'KIT'# Karlsruhe Institute of Technology 
da_preds.attrs['experiment'] = 'ESSD-benchmark'
da_preds.attrs['model'] = 'simple-NN'# in the paper this is referred to as DRN
da_preds.attrs['tier'] = 1
da_preds.attrs['version'] = 'v1.1'# 1
da_preds.attrs['dataset'] = 'hacky-phase'
da_preds.attrs['output'] = 'quantiles'


# In[8]:


da_preds.attrs


# In[9]:


file_name = f'{da_preds.tier}_{da_preds.experiment}_{da_preds.institution}_{da_preds.model}_{da_preds.version}'


# ### compare with example output format

# In[10]:


reference_out= xr.open_dataarray(f'{orig_data_path}/ESSD_benchmark_test_data_forecasts.nc')


# In[11]:


correct_forecast_lead_time = reference_out.step.values
correct_forecast_reference_time = reference_out.time.values


# ### correct coords

# In[12]:


da_preds.coords['forecast_lead_time'] = correct_forecast_lead_time
da_preds.coords['forecast_reference_time'] = correct_forecast_reference_time


# In[13]:


da_preds.coords['realization'] = da_preds.coords['realization'].astype('int')


# In[14]:


da_preds = da_preds.rename({'forecast_lead_time' : 'step', 'realization':'number', 
                            'forecast_reference_time' : 'time'})


# In[15]:


da_preds


# ### save predictions

# In[20]:


# save to file
da_preds.to_netcdf(f'{out_path}/{file_name}.nc')


