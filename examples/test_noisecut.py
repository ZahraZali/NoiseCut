import noisecut
import obspy


st= obspy.read('D10.DO.HH4..D.2012.080.000000')
hps_trace, spectrograms = noisecut.noisecut (st[0], ret_spectrograms= True)
noisecut.plot_noisecut_spectrograms (*spectrograms)





