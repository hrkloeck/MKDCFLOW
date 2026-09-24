#
# HRK
#
# re-structure the data into spectral windows (SPWD)
# and hanning smooth it
#
# -----

import casatasks
import sys

MSFILE      = sys.argv[1]
sing_ddir   = sys.argv[2]
sing_wdir   = sys.argv[3]
#
spectral_wd = sys.argv[4]
#
ms_name   = sing_ddir + MSFILE
#
# Note the data will be written into the data directory
#
ms_output = sing_ddir + MSFILE+'.hann.spwd'
#
#
casatasks.mstransform(vis=ms_name, regridms=True, nspw=int(spectral_wd), hanning=True, keepflags=True, outputvis=ms_output, datacolumn='data')

