#
# HRK
#
#
import casatasks
import sys
import json

MSFILE       = sys.argv[1]
sing_ddir    = sys.argv[2]
sing_wdir    = sys.argv[3]
#
jsonfile     = sys.argv[4]
field_id     = sys.argv[5]
spwds        = sys.argv[6]
#
ms_name      = sing_ddir + MSFILE
jsonfilename = sing_wdir + jsonfile


# ====================================
#
if jsonfilename.count('json') > 0:
        with open(jsonfilename) as f:
                d = json.load(f)
                source_name = d['SOURCES'][int(field_id)]
else:
    source_name = jsonfilename
#
print('\n - CASA split: ',source_name)
#
ms_outname = sing_ddir + MSFILE+'_'+source_name
#
if spwds == '0':
    casatasks.split(vis=ms_name,outputvis=ms_outname,keepmms=True,field=int(field_id),datacolumn='corrected',keepflags=True)
else:
    casatasks.split(vis=ms_name,outputvis=ms_outname,keepmms=True,field=int(field_id),datacolumn='corrected',keepflags=True,spw=spwds)

#
# ====================================
