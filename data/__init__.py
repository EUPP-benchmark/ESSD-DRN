import pandas as pd
import numpy as np


def normalize(data, method=None, shift=None, scale=None):
    result = np.zeros(data.shape)
    if method == "MAX":
        scale = np.max(data, axis=0)
        shift = np.zeros(scale.shape)
    for index in range(len(data[0])):
        result[:,index] = (data[:,index] - shift[index]) / scale[index]
    return result, shift, scale


def get_fcst_data_leadtime(path, leadtime):
    train_data = pd.read_feather(path = path + 'train_data_leadtime' + str(leadtime) + '.feather')
    test_data = pd.read_feather(path = path + 'test_data_leadtime' + str(leadtime) + '.feather')
    return train_data, test_data


def get_orog_data(path):
    return pd.read_csv(path)


def preprocess_data_train(train_data, orog_data):
    used_train_data = train_data.drop(['step'], axis=1)
    reordered_train_data = used_train_data.loc(axis=1)['year', 'time', 'station_id', 'obs', 
                                                       'model_land_usage', 'station_land_usage', 
                                                       'model_altitude', 'model_latitude', 
                                                       'model_longitude', 'station_altitude', 
                                                       'station_latitude', 'station_longitude', 
                                                       'number', 't2m']
    fcst_train_data = reordered_train_data.pivot(index=['year', 'time', 'station_id', 'obs', 
                                                        'model_land_usage', 'station_land_usage', 
                                                        'model_altitude', 'model_latitude', 
                                                        'model_longitude', 'station_altitude', 
                                                        'station_latitude', 'station_longitude'], 
                                                 columns="number", values="t2m")
    fcst_train_data = fcst_train_data.reset_index()
    
    ens_std_train = fcst_train_data.iloc[:,range(12,23)].std(axis=1)
    ens_mean_train = fcst_train_data.iloc[:,range(12,23)].mean(axis=1)
    
    input_train_data = fcst_train_data.iloc[:, list(range(4)) + list(range(6,12))]
    train_info = input_train_data.iloc[:,:4]
    
    input_train_data['t2m_std'] = ens_std_train
    input_train_data['t2m_mean'] = ens_mean_train

    fcst_train_doy = fcst_train_data['time'].dt.dayofyear
    input_train_data['doy'] = -np.cos(2 * np.pi * fcst_train_doy / 365)
    
    # convert the 2D vectors (model_land_usage, station_land_usage) into scalars land_usage (because embedding is applied on only 1D inputs)
    input_train_data['land_usage'] = (fcst_train_data['model_land_usage'] - 1) * 44 + fcst_train_data['station_land_usage']
    
    # add model orography data
    input_train_data_all = pd.merge(input_train_data, orog_data, on="station_id", validate="many_to_one")
    input_train_data_n = input_train_data_all.sort_values(by=['time', 'station_id'])
    
    train_features_raw = input_train_data_n.iloc[:, list([14])+list(range(4,13))].to_numpy()
    train_targets = input_train_data_n.iloc[:,3].to_numpy()
    train_IDs = input_train_data_n.iloc[:,2].to_numpy()
    train_lu = input_train_data_n.iloc[:,13].to_numpy()
    
    return train_features_raw, train_targets, train_IDs, train_lu, train_info
    
 
def preprocess_data_test(test_data, orog_data):
    leadtime = test_data['step'].loc[0]
    
    used_test_data = test_data.drop(['step'], axis=1)
    reordered_test_data = used_test_data.loc(axis=1)['time', 'station_id', 'obs', 'model_land_usage', 
                                                     'station_land_usage', 'model_altitude', 
                                                     'model_latitude', 'model_longitude', 
                                                     'station_altitude', 'station_latitude', 
                                                     'station_longitude', 'number', 't2m']
    fcst_test_data = reordered_test_data.pivot(index=['time', 'station_id', 'obs', 'model_land_usage', 
                                                      'station_land_usage', 'model_altitude', 
                                                      'model_latitude', 'model_longitude', 
                                                      'station_altitude', 'station_latitude', 
                                                      'station_longitude'], columns="number", values="t2m")
    fcst_test_data = fcst_test_data.reset_index()

    ens_std_test = fcst_test_data.iloc[:,range(11,62)].std(axis=1)
    ens_mean_test = fcst_test_data.iloc[:,range(11,62)].mean(axis=1)

    input_test_data = fcst_test_data.iloc[:, list(range(3)) + list(range(5,11))]
    test_info = input_test_data.iloc[:,:3]
    
    input_test_data['t2m_std'] = ens_std_test
    input_test_data['t2m_mean'] = ens_mean_test

    fcst_test_doy = fcst_test_data['time'].dt.dayofyear
    input_test_data['doy'] = -np.cos(2 * np.pi * fcst_test_doy / 365)

    # convert the 2D vectors (model_land_usage, station_land_usage) into scalars land_usage (because embedding is applied on only 1D inputs)
    input_test_data['land_usage'] = (fcst_test_data['model_land_usage'] - 1) * 44 + fcst_test_data['station_land_usage']
    
    # add model orography data
    input_test_data_all = pd.merge(input_test_data, orog_data, on="station_id", validate="many_to_one")
    input_test_data_n = input_test_data_all.sort_values(by=['time', 'station_id'])

    test_features_raw = input_test_data_n.iloc[:, list([13])+list(range(3,12))].to_numpy()
    test_targets = input_test_data_n.iloc[:,2].to_numpy()
    test_IDs = input_test_data_n.iloc[:,1].to_numpy()
    test_lu = input_test_data_n.iloc[:,12].to_numpy()
    
    return test_features_raw, test_targets, test_IDs, test_lu, test_info, leadtime

