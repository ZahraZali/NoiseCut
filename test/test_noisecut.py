import os
import noisecut
import obspy


def test_noisecut():

    print(__file__)

    fn = os.path.join(
        os.path.dirname(__file__),
        'D10.DO.HH4..D.2012.080.000000')

    st = obspy.read(fn)
    hps_trace, spectrograms = noisecut.noisecut(st[0], ret_spectrograms=True)
    noisecut.plot_noisecut_spectrograms(*spectrograms)
