# NoiseCut
[![DOI](https://zenodo.org/badge/478924343.svg)](https://zenodo.org/badge/latestdoi/478924343)

NoiseCut is a Python package for denoising seismic records. It is specifically developed for noise reduction of Ocean Bottom Seismometer (OBS) data from both horizontal and vertical components, however, it is able to separate long-lasting narrowband signals from different kinds of data. It works based on harmonic-percussive
separation algorithms (Zali et al., 2021).

## Links
Paper: https://doi.org/10.5194/se-14-181-2023

## Example of one day OBS signal
After installing the package, in order to denoise a signal you can use the following code. The outputs are the denoised signal and the spectrogram as below.The spectrogram shows only the frequency range of [0-1] Hz.

import noisecut                                                                                                                                                          
import obspy

st = obspy.read('D10.DO.HH4..D.2012.080.000000')                                                                                       
hps_trace, spectrograms = noisecut.noisecut(st[0], ret_spectrograms=True)                                                  
noisecut.plot_noisecut_spectrograms(*spectrograms)

![network architecture](Example-spectrograms.png)

## Installation

For the installation you need to clone the repository. Then run "python setup.py install" in the terminal. 
You need the Numpy version of 2.21.

## Licence

NoiseCut is licenced under the [GNU Affero General Public License
(AGPLv3)](LICENSE).

## Contact

* Author: Zahra Zali, zali@uni-potsdam.de
