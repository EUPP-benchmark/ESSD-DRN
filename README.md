# ESSD-DRN

Distributional regression network (DRN) scripts for the ESSD benchmark. 

The code is provided as supplementary material with
- The EUPPBench post-processing benchmark dataset v1.0, ...

# Details on the method

The DRN approach proposed by Rasp and Lerch (2018)[^fn1] is a neural network (NN) based method where the distribution parameters of the post-processed probabilistic forecasts are obtained as the output of the NN model. Our implementation for the EUPPBench closely follow Rasp and Lerch (2018)[^fn1] and use a NN with one hidden layer of 512 nodes. The input predictors of our NN model are listed in the following table, and all predictors except for the date information and the embedding are normalized to the range [0,1] using a min-max scalar before training. We assume a Guassian distribution for the post-processing temperature forecasts, and the NN model returns the mean and standard deviation of the distribution as outputs.

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
|**land_usage**| Combination of *model_land_usage* and *station_land_usage*, using a mapping from the 2D vector (*model_land_usage*, *station_land_usage*) to the 1D scalar *land_usage*|


[^fn1]: Rasp, S., and Lerch, S. (2018). Neural Networks for Postprocessing Ensemble Weather Forecasts. *Monthly Weather Review* 146, 11, 3885-3900, available from: <https://doi.org/10.1175/MWR-D-18-0187.1> [Accessed 19 December 2022]


# Data and usage

## Pre-processing data

## Implementing DRN

## Obtaining predictions

# Computational performance indication
