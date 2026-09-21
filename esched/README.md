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

Do some basic flagging using CASA

```
chmod 755 03_BASE_FLAGGING_CASA
```


```
condor_submit 03_FLAGGING_CASA.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD 
```



## Generate a averaged waterfall spectrum

These steps are part of an alternative aproach for flagging.

```
git clone https://github.com/hrkloeck/DASKMSWERKZEUGKASTEN.git
```


1. produce an averaged waterfall spectrum

```
chmod 755 04_AVERAGE_WATERFALL_SPECTRA
```


```
condor_submit 04_AVERAGE_WATERFALL_SPECTRA.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD FIELD_ID=0
```

2. 
```
chmod 755 05_GENERATE_WATERFALL_FLAGS
```

```
condor_submit 05_GENERATE_WATERFALL_FLAGS.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD AVG_FILE=PREFG_FID_0_J0408-6545_PREFG_DATA_FID_0__pickle.py
```


