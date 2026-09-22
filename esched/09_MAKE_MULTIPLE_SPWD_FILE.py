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
ms_output = sing_wdir + MSFILE+'.hann.spwd'
#
#
casatasks.mstransform(vis=ms_name, regridms=True, nspw=spectral_wd, hanning=True, keepflags=True, outputvis=ms_output, datacolumn='data')

