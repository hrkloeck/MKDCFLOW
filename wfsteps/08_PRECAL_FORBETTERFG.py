# 08/11/23
# HRK
#
# history:
#
# - Sarvesh original
# - HRK adapted for CASA with python in a singularity container 
# - changed model of lux cal
#
# singularity exec --bind ${PWD}:/data /media/scratch/Container_Build/HRK_CASA_6.5_DASK_WSC3.3.1024.simg python3 /data/8_PRECAL_FORBETTERFG.py
#
#
import casatasks
import CAL2GC_lib as CL
import shutil

msfile_name = '1678636873_sdp_l0_GS.ms'

flux_cal    = '*0408*'
refant      = 'm000'
myuvrange   = '>100m'

# ====================================
#
homedir   = '/data/'
out_dir   = '/data'
#
ms_name   = homedir + msfile_name

# Setjy in Stevens Reynolds model
#
# updated HRK 8/11/23
#
casatasks.setjy(vis=ms_name, field='*0408*', standard="manual",
      fluxdensity=[6.98620384013591, 0, 0, 0],
      spix=[-1.2897445398251446, -0.23527873971773555, 0.0860999999999989],
      reffreq='2.7GHz',
      scalebychan=True,
      usescratch=False)

# Setup some directories
#

K_cal = out_dir + '/delay.precal'
B_cal = out_dir + '/bandpass.precal'
G_cal = out_dir + '/gain.precal'






# =====================================================


# Solve for KGB solutions and apply to flux calibrators
#
casatasks.gaincal(vis=ms_name,
        field=flux_cal,
        caltable=K_cal,
        refant=refant,
        solint='inf',
        gaintype='K')
#
casatasks.gaincal(vis=ms_name,
        field=flux_cal,
        uvrange=myuvrange,
        caltable=G_cal,
        gaintype='G',
        solint='inf',
        refant=refant,
        calmode='p',
        minsnr=5,
        gainfield=[flux_cal],
        interp = ['nearest'],
        gaintable=[K_cal])
#
casatasks.bandpass(vis=ms_name,
        field=flux_cal,
        uvrange=myuvrange,
        caltable=B_cal,
        refant = refant,
        solint='inf',
        solnorm=False,
        minblperant=4,
        minsnr=3.0,
        bandtype='B',
        fillgaps=3,
        parang=False,
        gainfield=[flux_cal, flux_cal],
        interp = ['nearest', 'linear'],
        gaintable=[K_cal, G_cal])
#
casatasks.applycal(vis=ms_name,
         field=flux_cal,
         gaintable=[K_cal, G_cal, B_cal],
         interp=['nearest', 'nearest', 'linear'],
         parang=True, calwt=False, flagbackup=False)
#
casatasks.applycal(vis=ms_name,
         field='*0521*,*0252*',
         gaintable=[K_cal, B_cal],
         interp=['nearest', 'nearest'],
         gainfield=[flux_cal, flux_cal],
         parang=True, calwt=False, flagbackup=False)
#
# Do some additional flagging on the calibrated data
#
casatasks.flagdata(vis=ms_name, mode='summary', field=flux_cal)
#
casatasks.flagdata(vis=ms_name,
         field=flux_cal,
         datacolumn='corrected',
         flagbackup=False,
         mode='tfcrop',
         timecutoff=6.0, freqcutoff=5.0,
         timefit='poly', freqfit='line', flagdimension="freqtime",
         timedevscale=5., freqdevscale=5.,
         extendflags=False)
#
casatasks.flagdata(vis=ms_name,
         field=flux_cal,
         datacolumn='corrected',
         flagbackup=False,
         mode='rflag',
         timecutoff=5.0, freqcutoff=5.0,
         timefit="poly", freqfit="poly", flagdimension="freqtime",
         timedevscale=5., freqdevscale=5.,
         extendflags=False)
#
casatasks.flagdata(vis=ms_name, mode="extend", field=flux_cal,
         datacolumn="corrected", clipzeros=True, ntime="scan",
         extendflags=True, extendpols=True, flagbackup=False,
         growtime=90.0, growfreq=90.0, growaround=True, flagneartime=True, flagnearfreq=True)
#
casatasks.flagdata(vis=ms_name, mode='summary', field=flux_cal)

# store casa log file to current directory 
#
current_casa_log = CL.find_CASA_logfile(checkdir='HOME',homedir='')
shutil.move(current_casa_log,homedir)   
