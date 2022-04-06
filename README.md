# NoiseCut
OBS noise reduction from horizontal and vertical components using harmonic-percussive
separation algorithms

## Example of one day OBS signal

import noisecut

import obspy

st = obspy.read('D10.DO.HH4..D.2012.080.000000')
hps_trace, spectrograms = noisecut.noisecut(st[0], ret_spectrograms=True)
noisecut.plot_noisecut_spectrograms(*spectrograms)

![network architecture](Example-spectrograms.png)

## Installation

Find documentation and installation instructions in [NoiseCut's documentation
preview](https://NoiseCut.org/doc).

## Licence

NoiseCut is licenced under the [GNU Affero General Public License
(AGPLv3)](LICENSE).

## Contact

* Author: Zahra Zali, zali@uni-potsdam.de
