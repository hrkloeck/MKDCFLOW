# 08/11/23
# HRK
#
# history:
#
# - Sarvesh original
# - HRK adapted for CASA with python in a singularity container 
# - changed model of lux cal
#
# singularity exec --bind ${PWD}:/data /media/scratch/Container_Build/HRK_CASA_6.5_DASK_WSC3.3.1024.simg python3 /data/11_DO_FULL_CALIBRATION.py
#
#
import casatasks
import CAL2GC_lib as CL
import shutil

msfile_name = '1678636873_sdp_l0_GS.ms.hann.spw'

flux_cal    = '*0408*'
refant      = 'm000'
myuvrange   = '>100m'

# ====================================
#
homedir   = '/data/'
out_dir   = '/data/'
#
ms_name   = homedir + msfile_name


# Define the calibration tables
K_cal       = out_dir + '_delay.cal'
B_cal       = out_dir + '_bandpass.cal'
G_cal       = out_dir + '_gain.cal'
F_cal       = out_dir + '_fluxscale.cal'
T_cal       = out_dir + '_T.cal'
D_cal       = out_dir + '_leakage.cal'
D_dc_cal    = out_dir + '_leakage_dc.cal'
K_cross_cal = out_dir + '_kcross.cal'
X_dc_cal    = out_dir + '_Xf_dc.cal'
X_cal       = out_dir + '_Xf_new.cal'

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


# Solve for K
casatasks.gaincal(vis=ms_name,
        field=flux_cal,
        caltable=K_cal,
        refant=refant,
        solint='inf',
        gaintype='K',
        combine='')
# Solve for G
casatasks.gaincal(vis=ms_name,
        field='{}'.format(flux_cal),
        uvrange=myuvrange,
        caltable=G_cal,
        gaintype='G',
        solnorm=False,
        solint='40s',
        refant=refant,
        calmode='p',
        combine='',
        minsnr=5,
        gainfield=[flux_cal],
        interp = ['nearest'],
        gaintable=[K_cal])
# Solve for B
casatasks.bandpass(vis=ms_name,
        field=flux_cal,
        uvrange=myuvrange,
        caltable=B_cal,
        refant = refant,
        solint='inf',
        solnorm=False,
        minblperant=4,
        minsnr=3.0,
        combine='',
        bandtype='B',
        gainfield=[flux_cal, flux_cal],
        interp = ['nearest', 'nearest'],
        gaintable=[K_cal, G_cal])
casatasks.rmtables(K_cal)
# Solve for K
casatasks.gaincal(vis=ms_name,
        field=flux_cal,
        caltable=K_cal,
        refant=refant,
        solint='inf',
        gaintype='K',
        combine='',
        gainfield=[flux_cal, flux_cal],
        interp = ['nearest', 'nearest'],
        gaintable=[G_cal, B_cal])
casatasks.rmtables(G_cal)
# Solve for G
casatasks.gaincal(vis=ms_name,
        field='{}'.format(flux_cal),
        uvrange=myuvrange,
        caltable=G_cal,
        gaintype='G',
        solnorm=False,
        solint='60s',
        refant=refant,
        calmode='ap',
        combine='',
        minsnr=5,
        gainfield=[flux_cal, flux_cal],
        interp = ['nearest', 'nearest'],
        gaintable=[B_cal, K_cal])
# Solve for B
casatasks.rmtables(B_cal)
casatasks.bandpass(vis=ms_name,
        field=flux_cal,
        uvrange=myuvrange,
        caltable=B_cal,
        refant = refant,
        solint='inf',
        solnorm=False,
        minblperant=4,
        minsnr=3.0,
        combine='',
        bandtype='B',
        gainfield=[flux_cal, flux_cal],
        interp = ['nearest', 'nearest'],
        gaintable=[K_cal, G_cal])
casatasks.rmtables(K_cal)
# Solve for K
casatasks.gaincal(vis=ms_name,
        field=flux_cal,
        caltable=K_cal,
        refant=refant,
        solint='inf',
        gaintype='K',
        combine='',
        gainfield=[flux_cal, flux_cal],
        interp = ['nearest', 'nearest'],
        gaintable=[B_cal, G_cal])
# Using G_cal, derive fluxscale
casatasks.gaincal(vis=ms_name,
        field='*0252*,{}'.format(flux_cal),
        uvrange=myuvrange,
        caltable=T_cal,
        gaintype='T',
        solnorm=False,
        solint='inf',
        refant=refant,
        calmode='ap',
        combine='',
        minsnr=3,
        gainfield=[flux_cal, flux_cal, flux_cal],
        interp = ['linear', 'nearest', 'nearest'],
        gaintable=[B_cal, K_cal, G_cal])
casatasks.gaincal(vis=ms_name,
        field='*0521*',
        uvrange=myuvrange,
        caltable=T_cal,
        gaintype='T',
        solnorm=False,
        solint='inf',
        refant=refant,
        calmode='ap',
        combine='',
        minsnr=3,
        gainfield=[flux_cal, flux_cal, flux_cal],
        interp = ['linear', 'nearest', 'nearest'],
        gaintable=[B_cal, K_cal, G_cal],
        append=True)
casatasks.fluxscale(vis=ms_name,
          caltable=T_cal,
          fluxtable=F_cal,
          reference=flux_cal,
          transfer=['*0521*', '*0252*'],
          incremental=False)

# define pol and unpol calibrators, P&B2017 + updated pol properties 
# from NRAO web site 
# (https://science.nrao.edu/facilities/vla/docs/manuals/obsguide/modes/pol, 
# Table 7.2.7)
polarized_calibrators = {"3C138": {"standard": "manual",
                                       "fluxdensity": [8.33843],
                                       "spix": [-0.4981, -0.1552, -0.0102, 0.0223],
                                       "reffreq": "1.47GHz",
                                       "polindex": [0.078],
                                       "polangle": [-0.16755]},
                             "3C286": {"standard": "manual",
                                       "fluxdensity": [14.7172],
                                       "spix": [-0.4507, -0.1798, 0.0357],
                                       "reffreq": "1.47GHz",
                                       "polindex": [0.098],
                                       "polangle": [0.575959]},
                             }
# Add the polarization model of pol_cal to the MODEL_DATA column
pol_cal = '3C138'

casatasks.setjy(vis=ms_name,
      usescratch=False,
      scalebychan=True,
      field='*0521*',
      standard=polarized_calibrators[pol_cal]['standard'],
      fluxdensity=polarized_calibrators[pol_cal]['fluxdensity'],
      spix=polarized_calibrators[pol_cal]['spix'],
      reffreq=polarized_calibrators[pol_cal]['reffreq'],
      polindex=polarized_calibrators[pol_cal]['polindex'],
      polangle=polarized_calibrators[pol_cal]['polangle'])

# Solve for KCROSS
casatasks.gaincal(vis=ms_name,
        caltable=K_cross_cal,
        field='*0521*',
        uvrange=myuvrange,
        refant=refant,
        solint='inf',
        parang=True,
        combine='',
        gaintype='KCROSS',
        gaintable=[B_cal, G_cal, K_cal, T_cal],
        gainfield=['', '', '', '*0521*'],
        interp=['linear', 'linear', 'nearest', 'nearest'])

# Solve for polarization angle
# First solve for DC term that is constant across scans
# Next solve for Xf that is constant within a scan
casatasks.polcal(vis=ms_name,
       caltable=X_dc_cal,
       field='*0521*',
       uvrange=myuvrange,
       solint='inf',
       poltype='Xf',
       refant='',
       combine='',
       preavg=-1.,
       gaintable=[B_cal, G_cal, K_cal, K_cross_cal, T_cal],
       gainfield=['', '', '', '', '*0521*'],
       interp=['linear', 'linear', 'nearest', '', 'nearest'])
casatasks.polcal(vis=ms_name,
       caltable=X_cal,
       field='*0521*',
       uvrange=myuvrange,
       solint='inf',
       poltype='Xf',
       refant='',
       combine='scan',
       preavg=-1.,
       gaintable=[B_cal, G_cal, K_cal, K_cross_cal, X_dc_cal, T_cal],
       gainfield=['', '', '', '', '', '*0521*'],
       interp=['linear', 'linear', 'nearest', '', '', 'nearest'])

# Solve for leakage
# First solve for a DC term that is constant across all scans
# Then solve for a freq dependent term that is constant across a scan
casatasks.polcal(vis=ms_name,
       caltable=D_dc_cal,
       field=flux_cal,
       uvrange=myuvrange,
       combine='scan',
       solint='inf',
       poltype='D',
       refant='',
       gaintable=[B_cal, G_cal, K_cal, K_cross_cal, X_dc_cal, X_cal, T_cal],
       gainfield=[flux_cal, flux_cal, flux_cal, '', '', '', flux_cal],
       interp=['nearest', 'nearest', 'nearest', '', '', '','nearest'])
casatasks.polcal(vis=ms_name,
       caltable=D_cal,
       field=flux_cal,
       uvrange=myuvrange,
       combine='',
       solint='inf',
       poltype='Df',
       refant='',
       gaintable=[B_cal, G_cal, K_cal, D_dc_cal, K_cross_cal, X_dc_cal, X_cal, T_cal],
       gainfield=[flux_cal, flux_cal, flux_cal, '', '', '', '', flux_cal],
       interp=['nearest', 'nearest', 'nearest', '', '', '', '', 'nearest'])

# Apply to all calibrators
casatasks.applycal(vis=ms_name,
      field=flux_cal,
      gaintable=[K_cal, B_cal, F_cal, D_dc_cal, D_cal, K_cross_cal, X_cal, X_dc_cal, G_cal],
      interp=['nearest', 'linear', 'nearest', '', '', '', '', '', 'linear'],
      gainfield=['', '', flux_cal, '', '', '', '', '', ''],
      parang=True, calwt=False, flagbackup=False)
casatasks.applycal(vis=ms_name,
        field='*0521*',
        gaintable=[K_cal, B_cal, F_cal, D_dc_cal, D_cal, 
                   K_cross_cal, X_cal, X_dc_cal, G_cal],
        interp=['nearest', 'linear', 'nearest', '', '', '', '', '', 'linear'],
        gainfield=['', '', '*0252*', '', '', '', '', '', ''],
        parang=True, calwt=False, flagbackup=False)
casatasks.applycal(vis=ms_name,
      field='*0252*',
      gaintable=[K_cal, B_cal, F_cal, D_dc_cal, D_cal, K_cross_cal, X_cal, X_dc_cal, G_cal],
      interp=['nearest', 'linear', 'nearest', '', '', '', '', '', 'linear'],
      gainfield=['', '', '*0252*', '', '', '', '', '', ''],
      parang=True, calwt=False, flagbackup=False)

# Apply to target
casatasks.applycal(vis=ms_name,
      field='J0413-8000',
      gaintable=[K_cal, B_cal, F_cal, D_dc_cal, D_cal, K_cross_cal, X_cal, X_dc_cal, G_cal],
      interp=['nearest', 'linear', 'linear', '', '', '', '', '', 'linear'],
      gainfield=['', '', '*0252*', '', '', '', '', '', ''],
      parang=True, calwt=False, flagbackup=False)


# store casa log file to current directory 
#
current_casa_log = CL.find_CASA_logfile(checkdir='HOME',homedir='')
shutil.move(current_casa_log,homedir)   

