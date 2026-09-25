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

ms_name      = sing_ddir + MSFILE
jsonfilename = sing_wdir + jsonfile

with open(jsonfilename) as f:
        d = json.load(f)
        source_name = d['SOURCES'][int(field_id)]

#
# ====================================

# ====================================
#

for s in range(len(source_tosplit_idx)):
    #
    #
    print('\n - CASA split: ',source_name)
    #
    ms_outname = sing_ddir + MSFILE+'_'+source_name
    #
    casatasks.split(vis=ms_name,outputvis=ms_outname,keepmms=True,field=int(field_id),datacolumn='corrected',keepflags=True)

#
# ====================================
