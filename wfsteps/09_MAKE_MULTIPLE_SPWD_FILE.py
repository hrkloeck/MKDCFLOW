#
# do some initial flagging
#

#
# singularity exec --bind ${PWD}:/data /media/scratch/Container_Build/HRK_CASA_6.5_DASK_WSC3.3.1024.simg python3 /data/09_MAKE_MULTIPLE_SPWD_FILE.py
#

import casatasks
import CAL2GC_lib as CL
import shutil

spectral_wd = 16

homedir = '/data/'

ms_name   = homedir + '1678636873_sdp_l0_GS.ms'
ms_output = homedir + '1678636873_sdp_l0_GS.ms.hann.spw'

casatasks.mstransform(vis=ms_name, regridms=True, nspw=spectral_wd, hanning=True, keepflags=True, outputvis=ms_output, datacolumn='data')

# store casa log file to current directory 
#
current_casa_log = CL.find_CASA_logfile(checkdir='HOME',homedir='')
shutil.move(current_casa_log,homedir)    

