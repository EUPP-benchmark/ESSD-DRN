# ESSD-DRN

Distributional regression network (DRN) scripts for the ESSD benchmark. 

The code is provided as supplementary material with
- The EUPPBench post-processing benchmark dataset v1.0, ...

# Details on the method

The DRN approach proposed by Rasp and Lerch (2018)[^fn1] is a neural network (NN) based method where the distribution parameters of the post-processed probabilistic forecasts are obtained as the output of the NN model. Our implementation for the EUPPBench closely follow Rasp and Lerch (2018)[^fn1] and use a NN with one hidden layer of 512 nodes. The input predictors of our NN model are listed in the following table, and all predictors except for the date information and the embedding are normalized to the range [0,1] using a min-max scalar before training. We assume a Guassian distribution for the post-processing temperature forecasts, and the NN model returns the mean and standard deviation of the distribution as outputs. For each lead time, a single NN model is estimated jointly for all stations, using the CRPS as a custom loss function. The model predictions are made locally adaptive by the use of embeddings of both the station identifiers and the summarized land usage information. We repeat the model estimation for 10 times and take the average outputs to get the final parameters of the post-processed distributional forecasts.

|Predictor| Description|
|-------------|---------------|
|**t2m_mean**| Mean of raw 2-m temperature ensemble forecasts|
|**t2m_std**| Standard deviation of raw 2-m temperature ensemble forecasts|
|model_altitude| Altitude of the model grid point given by a high-resolution (100m) Digital Elevation Model|
|model_latitude| Latitude of the model grid point given by a high-resolution (100m) Digital Elevation Model|
|model_longitude| Longitude of the model grid point given by a high-resolution (100m) Digital Elevation Model|
|station_altitude| Altitude of the weather station|
|station_latitude| Latitude of the weather station| 
|station_longitude| Longitude of the weather station|
|model_orog| model orography, i.e. the average grid box altitude in the model|
|**doy**| Sine-transformed value of the day of the year|

|Predictor for embedding| Description|
|-------------|---------------|
|station_id| Identification number of weather stations in the dataset|
|model_land_usage| Land usage of the model grid point|
|station_land_usage| Land usage of the weather station|
|**land_usage**| Summarized land usage information combining both *model_land_usage* and *station_land_usage*, using a mapping from the 2D vector (*model_land_usage*, *station_land_usage*) to the 1D scalar *land_usage*|

Our NN model is built upon the Keras[^fn2] framework in Python, and the detailed hyper-parameter choices are described as follows:

|Hyper-parameter of the NN model| Value|
|-------------|---------------|
|Embedding size of the *station_id*| 2|
|Embedding size of the *land_usage*| 4|
|Optimizer| Adam|
|Learning rate| 0.005|
|Batch size| 4096|
|Early stopping| With patience of 2 epochs and minimum delta of 0.005 on mornitoring the training loss|
|Maximum number of training epochs| 50|

[^fn1]: Rasp, S., and Lerch, S. (2018). Neural Networks for Postprocessing Ensemble Weather Forecasts. *Monthly Weather Review* 146, 11, 3885-3900, available from: <https://doi.org/10.1175/MWR-D-18-0187.1> [Accessed 19 December 2022]
[^fn2]: <https://keras.io/>

# Data and usage

The scripts are build for the ESSD benchmark dataset, which could be downloaded following the instructions on the [GitHub repository](https://github.com/EUPP-benchmark/ESSD-benchmark-datasets).

## Pre-processing data

The original ESSD benchmark dataset is in the NetCDF format, and we need to further pre-process it into the format that fit our DRN scripts.

**TO BE ADDED:** The part for trainsforming NetCDF format into feather format

The transformed feather file includes forecast information for all 21 lead times, and we need to further split them regarding different lead time for the model training. The `data_preprocess.py` script in the `data-preprocess` folder includes the codes for implementation.

## Implementing DRN

The DRN approach could be done by running the `DRN_pp.py` script in the home directory, note that the corresponding path of files need to be changed accordingly.

## Obtaining predictions

The output of NN models are the parameters of a Gaussian distribution, and we further run the  `get_predictions.R` script to generate 51 equi-quantile samples from the distribution as the post-processed ensemble forecasts.

**CHECK** The output ensemble forecasts are in the feather format, and need to be further transformed back to the netCDF format using ...

# Computational performance indication

The computation was done with 40 CPUs (Intel(R) Xeon(R) CPU E5-2680 v3 @ 2.50GHz) with 236 Gb of RAM. Training 21 NN models for different lead times takes approximately 2 hours in total.

