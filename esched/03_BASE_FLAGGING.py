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
# Preflag steps
#

# Flag autocorrelations
#
casatasks.flagdata(vis=ms_name, mode='manual', autocorr=True, flagbackup=False)

# Backup flag data
#
casatasks.flagmanager(vis=ms_name, mode='save', versionname='preflag_casa')
casatasks.flagdata(vis=ms_name, mode='summary')

