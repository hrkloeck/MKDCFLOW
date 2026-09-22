# A step by step workflow to run on Edgar 

Basic steps to submit:

```
bash
```

```
mkdir condor_logs
```

```
mkdir -p ${USER}/.casa/data 
```


## Obtain information of the observation

```
 git clone https://github.com/hrkloeck/daskmsASTROKIT.git
```

```
chmod 755 01_OBS_INFORMATION
```

```
condor_submit 01_OBS_INFORMATION.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD
```

## Produce some diagnostic plots

```
chmod 755 02_OBS_DIAGNOSTIC_PLOTS
```

```
condor_submit 02_OBS_DIAGNOSTIC_PLOTS.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD
```

## View diagnostic plots

```
chmod 755 00_VIEW_PNG_IMAGES
```

```
./00_VIEW_PNG_IMAGES ${PWD} FILE_NAME.png
```


## Flagging

### Basic Flagging

Do some basic flagging (thresholding, on zeros, shadowing) using CASA

```
chmod 755 03_BASE_FLAGGING_CASA
```


```
condor_submit 03_FLAGGING_CASA.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD 
```



### Flagging on the waterfall spectrum

These steps are part of an additional aproach for flagging.

```
git clone https://github.com/hrkloeck/DASKMSWERKZEUGKASTEN.git
```


1. Generate an baseline averaged waterfall spectrum and store it in a pickle
   file

```
chmod 755 04_AVERAGE_WATERFALL_SPECTRA
```


```
condor_submit 04_AVERAGE_WATERFALL_SPECTRA.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD FIELD_ID=0
```

2.  Generate flags on the waterfall spectrum 

```
chmod 755 05_GENERATE_WATERFALL_FLAGS
```

```
condor_submit 05_GENERATE_WATERFALL_FLAGS.sub WORK_PATH=$PWD AVG_FILE=PREFG_FID_0_J0408-6545_PREFG_DATA_FID_0__pickle.py
```

3. Flag the MS File by applying the average mask

```
chmod 755 06_APPLY_FLAGS
```

```
condor_submit 06_APPLY_FLAGS.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD FG_FILE=PLT_J0408-6545_FG_MASK_PREFG_FID_0_J0408-6545_PREFG_DATA_FID_0__pickle.py_pickle.py
```


4. Plot waterfall spectrum to check if FG's has been applied (optional)

```
chmod 755 07_AVERAGE_WATERFALL_SPECTRA
```


```
condor_submit 07_AVERAGE_WATERFALL_SPECTRA.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD FIELD_ID=0
```


### Flagging based on pre-calibrated (corrected) data

```
chmod 755 08_PRE_CAL_ADVANCE_FG
```


```
condor_submit 08_PRE_CAL_ADVANCE_FG.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD 
```


## Start of the 1GC Calibration Sequence

