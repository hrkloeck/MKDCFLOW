
import casatasks
import CAL2GC_lib as CL
import shutil

#
# writes out only data on good scans 
#

good_scans = "2,4,6,8,10,11,13,15,17,19,21,23,25,27,29,31,32,33"

homedir = '/data/'
#
ms_name    = homedir + '1678636873_sdp_l0.ms'
ms_outname = homedir + '1678636873_sdp_l0_GS.ms'

# writes out phase calibrator source
#
casatasks.mstransform(vis=ms_name,outputvis=ms_outname,scan=good_scans,keepflags=True,datacolumn='data')

# store casa log file to current directory 
#
current_casa_log = CL.find_CASA_logfile(checkdir='HOME',homedir='')
shutil.move(current_casa_log,homedir)    


