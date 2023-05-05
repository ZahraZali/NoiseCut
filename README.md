# NoiseCut
[![DOI](https://zenodo.org/badge/478924343.svg)](https://zenodo.org/badge/latestdoi/478924343)

NoiseCut is a Python package for denoising seismic records and specializes in denoising Ocean Bottom Seismometer (OBS) data. It effectively separates long-lasting narrowband signals from broadband transients using harmonic-percussive separation algorithms (Zali et al., 2021 & Zali et al., 2023). The advantage of NoiseCut is that it preserves the earthquake signal with its entire frequency and amplitude after denoising.

![example](https://user-images.githubusercontent.com/50201021/235652233-33ce7bdc-d717-4a9b-bef9-05bb524026ff.png)


## Links
Paper: https://se.copernicus.org/articles/14/181/2023/se-14-181-2023.pdf

Paper: https://pubs.geoscienceworld.org/ssa/srl/article/92/6/3668/606262/Volcanic-Tremor-Extraction-and-Earthquake

## Usage example
After installing the package to denoise a signal, you can use the following code. Outputs are the denoised signal and a figure showing the spectrogram of the input signal, the separated noise, and the denoised signal in the frequency range of [0-1] Hz.

import noisecut                                                                                                                                                         
import obspy

```
st = obspy.read('file_name')
hps_trace, spectrograms = noisecut.noisecut(st[0], ret_spectrograms=True)
noisecut.plot_noisecut_spectrograms(*spectrograms)
```

## Installation instructions

You can clone the public repository:
```
git clone https://github.com/ZahraZali/NoiseCut
```
Once you have a copy of the source, you can cd to NoiseCut directory and install it with:
```
python setup.py install
```
You need the Numpy version of 2.21.

## Licence

NoiseCut is licenced under the [GNU Affero General Public License
(AGPLv3)](LICENSE).

## Contact

* Developer: Zahra Zali, zali@gfz-potsdam.de
