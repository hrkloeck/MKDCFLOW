#
# Doing some initial flagging
#
import casatasks
import sys

MSFILE      = sys.argv[1]
sing_ddir   = sys.argv[2]
sing_wdir   = sys.argv[3]

ms_name   = sing_ddir + MSFILE
ms_output = sing_wdir + MSFILE+'.OBSINFO'


# threshold to flag bad data
#
UPDLIMT = 100.0

# Backup flag data
#
casatasks.flagmanager(vis=ms_name, mode='save', versionname='raw')
casatasks.flagdata(vis=ms_name, mode='summary')

#
# Base Flagging Steps
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

# 5. Flag based on upper limit
casatasks.flagdata(vis=ms_name, mode='clip', clipminmax=[0.0,UPDLIMT])


# Backup flag data
#
casatasks.flagmanager(vis=ms_name, mode='save', versionname='preflag_casa')
casatasks.flagdata(vis=ms_name, mode='summary')

