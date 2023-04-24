import pandas as pd
import numpy as np
import datetime

data_path='../data-feather/'

## Preprocessing training data

# read data
train_data = pd.read_feather(data_path+'ESSD_benchmark_training_data.feather')

# remove rows with missing data
used_data_train = train_data.dropna()

# remove duplicated columns
used_data_train = used_data_train.drop(['station_name', 'land_usage', 'altitude', 'latitude', 'longitude'], axis=1)

# spilt the dataset by different lead time, and save the files
df_steps = pd.DataFrame(np.unique(used_data_train['step']))

for k in range(21):
    print(k)
    
    df_selected = used_data_train[used_data_train['step'] == df_steps[0][k]]
    data_saved = df_selected.reset_index(drop=True)

    data_saved.to_feather(data_path+'train_data_leadtime' + str(k) + '.feather') 


## Preprocessing test data

# read data
test_data = pd.read_feather(data_path+'ESSD_benchmark_test_data.feather')

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

    data_saved.to_feather(data_path+'test_data_leadtime' + str(k) + '.feather') 
