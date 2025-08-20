# NoiseCut
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7339551.svg)](https://doi.org/10.5281/zenodo.7339551)

NoiseCut is a Python package for denoising seismic records and specializes in denoising Ocean Bottom Seismometer (OBS) data. It effectively separates long-lasting narrowband signals from broadband transients using harmonic-percussive separation algorithms (Zali et al., 2021 & Zali et al., 2023). The advantage of NoiseCut is that it preserves the earthquake signal with its entire frequency and amplitude after denoising.

![example](https://user-images.githubusercontent.com/50201021/235652233-33ce7bdc-d717-4a9b-bef9-05bb524026ff.png)


## Citations and Links

When using this package, please cite the following works:

1. **Zali, Z., Rein, T., Krüger, F., Ohrnberger, M., & Scherbaum, F.** (2023).  
   *Ocean bottom seismometer (OBS) noise reduction from horizontal and vertical components using harmonic–percussive separation algorithms.*  
   *Solid Earth, 14*(2), 181–195.  
   [https://doi.org/10.5194/se-14-181-2023](https://doi.org/10.5194/se-14-181-2023)  

2. **Zali, Z., Ohrnberger, M., Scherbaum, F., Cotton, F., & Eibl, E. P.** (2021).  
   *Volcanic tremor extraction and earthquake detection using music information retrieval algorithms.*  
   *Seismological Research Letters, 92*(6), 3668–3681.  
   [https://doi.org/10.1785/0220210016](https://doi.org/10.1785/0220210016)  


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
You need the Numpy version <= 1.21.

## Licence

NoiseCut is licenced under the [GNU Affero General Public License
(AGPLv3)](LICENSE).

## Contact

* Developer: Zahra Zali, zali@gfz-potsdam.de
