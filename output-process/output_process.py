import pandas as pd
import numpy as np
import datetime

# specify path
path = '../data-feather/'
new_path = '../data-csv/'

# predictions for each lead time:
for k in range(21):

    preds = pd.read_feather(path + 'orog_pred_leadtime' + str(k) + '.feather')

    preds_df = preds.drop(['index'], axis=1)
    preds_df = preds_df.rename(columns={'time': 'forecast_reference_time'})
    preds_df['forecast_lead_time'] = k
    preds_df = preds_df.loc(axis=1)['station_id', 'forecast_lead_time', 'forecast_reference_time', 't2m_mean', 't2m_std']

    preds_df.to_csv(new_path + 'orog_pred_leadtime' + str(k) + '.csv', index=False)

    print(k)

# repredictions for each lead time
for k in range(21):

    preds = pd.read_feather(path + 'orog_repred_leadtime' + str(k) + '.feather')

    preds_df = preds.drop(['index'], axis=1)
    preds_df = preds_df.rename(columns={'time': 'forecast_reference_time'})
    preds_df['forecast_lead_time'] = k
    preds_df = preds_df.loc(axis=1)['station_id', 'forecast_lead_time', 'forecast_reference_time', 't2m_mean', 't2m_std']

    preds_df.to_csv(new_path + 'orog_repred_leadtime' + str(k) + '.csv', index=False)

    print(k)
