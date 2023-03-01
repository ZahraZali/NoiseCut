# NoiseCut
[![DOI](https://zenodo.org/badge/478924343.svg)](https://zenodo.org/badge/latestdoi/478924343)

NoiseCut is a Python package for denoising seismic records. It is specifically developed for noise reduction of Ocean Bottom Seismometer (OBS) data from both horizontal and vertical components, however, it is able to separate long-lasting narrowband signals from different kinds of data. It works based on harmonic-percussive
separation algorithms (Zali et al., 2021 & Zali et al., 2023).

## Links
Paper: https://se.copernicus.org/articles/14/181/2023/se-14-181-2023.pdf

## Example of NoiseCut application
After installing the package, in order to denoise a signal you can use the following code. The outputs are the denoised signal and the spectrogram as below. The spectrogram shows frequency range of [0-1] Hz.

import noisecut                                                                                                                                                          
import obspy

st = obspy.read('file_name')                                                                                       
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

* Developer: Zahra Zali, zali@uni-potsdam.de
