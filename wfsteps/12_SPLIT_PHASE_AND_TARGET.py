# 08/11/23
# HRK
#
# history:
#
#
# singularity exec --bind ${PWD}:/data /media/scratch/Container_Build/HRK_CASA_6.5_DASK_WSC3.3.1024.simg python3 /data/12_SPLIT_PHASE_AND_TARGET.py
#
#
import casatasks
import CAL2GC_lib as CL
import shutil

# ===== define what to write out
#
msfile_name = '1678636873_sdp_l0_GS.ms.hann.spw'

# sources in MS file
#
source_tosplit_idx = [1,2]
obs_sources        = ['J0521+1638', 'J0252-7104', 'J0413-8000', 'J0408-6545']
ms_file_extention  = '_band4_cald.ms'
#
#
homedir   = '/data/'
out_dir   = '/data'
#
# ====================================

# ====================================
#
# write the stuff
#
ms_name   = homedir + msfile_name

for s in range(len(source_tosplit_idx)):
    #
    #
    print('\n - CASA split: ',obs_sources[source_tosplit_idx[s]])
    #
    ms_outname = homedir + obs_sources[source_tosplit_idx[s]]+ms_file_extention
    casatasks.split(vis=ms_name,outputvis=ms_outname,keepmms=True,field=obs_sources[source_tosplit_idx[s]],datacolumn='corrected',keepflags=True)

# store casa log file to current directory 
#
current_casa_log = CL.find_CASA_logfile(checkdir='HOME',homedir='')
shutil.move(current_casa_log,homedir)   
#
# ====================================
