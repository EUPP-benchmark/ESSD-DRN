# ESSD-DRN

This repository provides Python code for implementation of the distributional regression network (DRN) post-processing method, accompanying the EUPPBench post-processing benchmark dataset v1.0.

# Details on the DRN setup

The DRN approach proposed by Rasp and Lerch (2018)[^fn1] is a neural network (NN) based method where the distribution parameters of the post-processed forecast distribution are obtained as the output of a NN. Our implementation for EUPPBench closely follows Rasp and Lerch (2018)[^fn1] and uses a NN with one hidden layer of 512 nodes. The input predictors of our NN model are listed in the following table. All predictors except for the date information and the embedding are normalized to the range [0,1] using a min-max scaler before training. We assume a Gaussian distribution for the post-processed temperature forecasts, and the NN model returns mean and standard deviation of the distribution as outputs. For each lead time, a separate NN model is estimated jointly for all stations, using the CRPS as a custom loss function. The model predictions are made locally adaptive by using embeddings of both the station identifiers and the summarized land usage information. We repeat the model estimation 10 times and take the average over the outputs of all runs as the final parameters of the post-processed distributional forecasts.

|Predictor| Description|
|-------------|---------------|
|**`t2m_mean`**| Mean of raw 2-m temperature ensemble forecasts|
|**`t2m_std`**| Standard deviation of raw 2-m temperature ensemble forecasts|
|`model_altitude`| Altitude of the model grid point given by a high-resolution (100m) Digital Elevation Model|
|`model_latitude`| Latitude of the model grid point given by a high-resolution (100m) Digital Elevation Model|
|`model_longitude`| Longitude of the model grid point given by a high-resolution (100m) Digital Elevation Model|
|`station_altitude`| Altitude of the weather station|
|`station_latitude`| Latitude of the weather station| 
|`station_longitude`| Longitude of the weather station|
|`model_orog`| model orography, i.e. the average grid box altitude in the model|
|**`doy`**| Sine-transformed value of the day of the year|

|Predictor for embedding| Description|
|-------------|---------------|
|`station_id`| Identification number of weather station in the dataset|
|*`model_land_usage`*| Land usage of the model grid point|
|*`station_land_usage`*| Land usage of the weather station|
|**`land_usage`**| Summarized land usage information combining both *`model_land_usage`* and *`station_land_usage`*, using a mapping from the 2D vector (*`model_land_usage`*, *`station_land_usage`*) to the 1D scalar *`land_usage`*|

Our NN model is built using the Keras[^fn2] framework in Python. The specific hyper-parameter choices for our model are shown in the following table:

|Hyper-parameter of the NN model| Value|
|-------------|---------------|
|Embedding size of `station_id`| 2|
|Embedding size of `land_usage`| 4|
|Optimizer| Adam|
|Learning rate| 0.005|
|Batch size| 4096|
|Early stopping| With patience of 2 epochs and minimum delta of 0.005 on monitoring the training loss|
|Maximum number of training epochs| 50|

[^fn1]: Rasp, S., and Lerch, S. (2018). Neural Networks for Postprocessing Ensemble Weather Forecasts. *Monthly Weather Review* 146, 11, 3885-3900, available from: <https://doi.org/10.1175/MWR-D-18-0187.1> [Accessed 19 December 2022]
[^fn2]: <https://keras.io/>

# Data and implementation details

The scripts are built for the ESSD benchmark dataset, which can be downloaded following the instructions on the [GitHub repository](https://github.com/EUPP-benchmark/ESSD-benchmark-datasets).

## Data pre-processing

In order to run our DRN scripts on the ESSD benchmark dataset we had to adapt the data format. First, we combined reforecast and observation data and saved it to separate feather files for training and testing. The respective code is in `train_netCDF_to_feather.ipynb` and `test_netCDF_to_feather.ipynb` in the  `/data-preprocess/` folder. The transformed `.feather` files include forecast information for all 21 lead times. We further split them regarding different lead time using the `data_preprocess.py` script from the `/data-preprocess/` folder.

## Training and producing predictions of the DRN model

The DRN model can be run by executing the `DRN_pp.py` script in the home directory. Note that file paths have to be changed accordingly.

The output of the NN models are the parameters of a Gaussian distribution. The scripts in the `/output-process/` folder are used to obtain the final predictions in the required format. `output_process.py` adapts the format of the predictions to prepare for the following steps: First,`generate_fcst.R` generates samples from the distribution as the post-processed ensemble forecasts for each lead time in the form of 51 equi-distant quantiles. Then, `combine_fcst.R` combines the post-processed forecasts for all lead times.

The predictions are transformed to the required `netCDF` format and relevant meta-data is added in `feather_to_netCDF.ipynb`.

# Computational performance indication

The computation was done with 40 CPUs (Intel(R) Xeon(R) CPU E5-2680 v3 @ 2.50GHz) with 236 Gb of RAM. Training the 21 DRN models in the setup described above for all lead times takes approximately 2 hours in total.

