#
# do some initial flagging
#

import casatasks
import CAL2GC_lib as CL
import shutil

homedir = '/data/'

ms_name = homedir + '1678636873_sdp_l0_GS.ms'

# threshold to flag bad data
#
UPDLIMT = 100.0

# Backup flag data
#
casatasks.flagmanager(vis=ms_name, mode='save', versionname='raw')
casatasks.flagdata(vis=ms_name, mode='summary')

#
# Preflag steps
#

# Flag autocorrelations
#
casatasks.flagdata(vis=ms_name, mode='manual', autocorr=True, flagbackup=False)

# Flag for shadowing
casatasks.flagdata(vis=ms_name, mode='shadow', flagbackup=False)

# 3. Flag edge channels
casatasks.flagdata(vis=ms_name, spw='0:0', flagbackup=False, mode='manual')

# 4. Clip for zeros
casatasks.flagdata(vis=ms_name, flagbackup=False, mode='clip', clipzeros=True)

# Flag based on upper limit
casatasks.flagdata(vis=ms_name, mode='clip', clipminmax=[0.0,UPDLIMT])

# Backup flag data
#
casatasks.flagmanager(vis=ms_name, mode='save', versionname='preflag_casa')
casatasks.flagdata(vis=ms_name, mode='summary')

# store casa log file to current directory 
#
current_casa_log = CL.find_CASA_logfile(checkdir='HOME',homedir='')
shutil.move(current_casa_log,homedir)    
