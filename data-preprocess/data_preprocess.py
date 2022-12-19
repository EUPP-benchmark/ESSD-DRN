import pandas as pd
import numpy as np
import datetime


## Preprocessing test data

# read data
test_data = pd.read_feather('/Data/eumetnet/ESSD_benchmark_feather/ESSD_benchmark_test_data.feather')

# remove rows with missing data
used_data_test = test_data.dropna()

# remove duplicated columns
used_data_test = used_data_test.drop(['station_name', 'land_usage', 'altitude', 'latitude', 'longitude'], axis=1)

# spilt the dataset by different lead time, and save the files
df_steps = pd.DataFrame(np.unique(used_data_test['step']))

for k in range(21):
    print(k)
    
    df_selected = used_data_test[used_data_test['step'] == df_steps[0][k]]
    data_saved = df_selected.reset_index(drop=True)

    data_saved.to_feather('/Data/eumetnet/eumetnet_temp/new/test_data_leadtime' + str(k) + '.feather') 


## Preprocessing test data

# read data
test_data = pd.read_feather('/Data/eumetnet/ESSD_benchmark_feather/ESSD_benchmark_test_data.feather')

# remove rows with missing data
used_data_test = test_data.dropna()

# remove duplicated columns
used_data_test = used_data_test.drop(['station_name', 'land_usage', 'altitude', 'latitude', 'longitude'], axis=1)

# spilt the dataset by different lead time, and save the files
df_steps = pd.DataFrame(np.unique(used_data_test['step']))

for k in range(21):
    print(k)
    
    df_selected = used_data_test[used_data_test['step'] == df_steps[0][k]]
    data_saved = df_selected.reset_index(drop=True)

    data_saved.to_feather('/Data/eumetnet/eumetnet_temp/new/test_data_leadtime' + str(k) + '.feather') 