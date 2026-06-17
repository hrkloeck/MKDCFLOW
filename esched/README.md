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

```
 git clone https://github.com/hrkloeck/daskmsASTROKIT.git
```

```
chmod 755 01_OBS_INFORMATION
```

```
condor_submit 01_OBS_INFORMATION.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD
```


## Flagging


## Flagging

Just does basic flagging
```
condor_submit 03_FLAGGING_CASA.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD 
```

Sequence of jobs to be done

```
condor_submit 04_FLAGGING_HRK.sub DATA_FILE=1678454471_sdp_l0.ms DATA_PATH=/bEDD/MPLUS-WORKONDATA WORK_PATH=$PWD FIELD_ID=0
```

