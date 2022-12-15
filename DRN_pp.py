import pandas as pd
import numpy as np
import tensorflow as tf

from data import normalize, get_fcst_data_leadtime, get_orog_data, preprocess_data_train, preprocess_data_test
from model.drn_model import drn, drn_pp
from model.crps_function import crps_cost_function, crps_normal


f = open('./model_training.txt','w') # or None


def main():
    
    for n_leadtime in range(21):
        
        train_data, test_data = get_fcst_data_leadtime(path='/Data/eumetnet/eumetnet_temp/new/', leadtime=n_leadtime)
        model_orog = get_orog_data(path='/home/chen_jieyu/eumetnet/model_orog.csv')
        
        train_features_raw, train_targets, train_IDs, train_lu, train_info = preprocess_data_train(train_data, model_orog)
        test_features_raw, test_targets, test_IDs, test_lu, test_info, leadtime = preprocess_data_test(test_data, model_orog)
        
        # normalize data
        train_features = train_features_raw.copy()
        test_features = test_features_raw.copy()
        train_features[:,:9], train_shift, train_scale = normalize(train_features_raw[:,:9], method="MAX")
        test_features[:,:9] = normalize(test_features_raw[:,:9], shift=train_shift, scale=train_scale)[0]
        
        n_features = train_features.shape[1]
        emb_size_id = 2
        max_id = int(np.max([train_IDs.max(), test_IDs.max()]))
        emb_size_lu = 4
        max_lu = int(np.max([train_lu.max(), test_lu.max()]))
    
        nreps = 10
        
        trn_scores = []
        test_scores = []
        preds = []
        repred = []
        trn_times = []
        test_times = []
        
        model = drn(n_features, max_id, emb_size_id, max_lu, emb_size_lu)
        data = [train_features, train_IDs, train_lu, train_targets, test_features, test_IDs, test_lu, test_targets]
        loss_fn = crps_cost_function
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor = 'loss', min_delta = 0.005, patience = 2, restore_best_weights = True)
        
        # training multiple models in a loop
        for i in range(nreps):
            print(f'Repetition {i}')
            
            training_time, predicting_time, reprediction, prediction, training_score, test_score = drn_pp(model, data, loss_fn, early_stopping)
            
            trn_scores.append(training_score)
            test_scores.append(test_score)
            preds.append(prediction)
            repred.append(reprediction)
            trn_times.append(training_time)
            test_times.append(predicting_time)
    
        preds = np.array(preds)
        preds[:, :, 1] = np.abs(preds[:, :, 1]) # Make sure std is positive
        mean_preds = np.mean(preds, 0)
        
        repred = np.array(repred)
        repred[:, :, 1] = np.abs(repred[:, :, 1]) # Make sure std is positive
        mean_repred = np.mean(repred, 0)
        
        mean_preds_df = pd.DataFrame(mean_preds)
        mean_repred_df = pd.DataFrame(mean_repred)
        
        train_combine = pd.concat([train_info, mean_repred_df], axis=1) 
        test_combine = pd.concat([test_info, mean_preds_df], axis=1)
        
        train_combine = train_combine.rename(columns={0: 't2m_mean', 1: 't2m_std'})
        test_combine = test_combine.rename(columns={0: 't2m_mean', 1: 't2m_std'})
        
        fcst_data_leadtime_path = '/Data/eumetnet/eumetnet_temp/new/'
        train_combine.reset_index().to_feather(fcst_data_leadtime_path + 'orog_repred_leadtime' + str(n_leadtime) + '.feather')
        test_combine.reset_index().to_feather(fcst_data_leadtime_path + 'orog_pred_leadtime' + str(n_leadtime) + '.feather')
        
        # evaluate ensemble of models
        ens_score = crps_normal(mean_preds[:, 0], mean_preds[:, 1], test_targets).mean()
        
        print(f'Lead time = {leadtime}; \nEnsemble test score = {ens_score}', file=f)
        print('\nInformation on the 10 repetitions of the DRN model:', file=f)
        print(f'\nTraining losses: {trn_scores}; \nTest losses: {test_scores}', file=f)
        print(f'\nProcessing time of training (in seconds): {trn_times}; \nProcessing time of predicting (in seconds): {test_times}', file=f)


        
if __name__ == '__main__':
    # execute main function only if script is called as the __main__ script
    main()


if f is not None:
    f.close()