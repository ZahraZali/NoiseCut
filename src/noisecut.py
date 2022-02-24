# -----------------------------------------------------------------------------
# NoiseCut
#
# This file is part of the NoiseCut library. For licensing information see the
# accompanying file `LICENSE`.
# -----------------------------------------------------------------------------


import numpy as np
import librosa
from obspy import read, Trace, Stream
import librosa.display
import matplotlib.pyplot as plt


def noisecut(file, component, plotspec='no'):
    '''
    Reduce noise from all the components of the OBS data using HPS noise
    reduction algorithms.
    '''

    trace = read(file)
    x = trace[component].data
    y = x.astype(float)

    sr = 16000
    hop_length = 4096
    win_length = 16384
    n_fft = 16384

    # Compute the spectrogram amplitude and phase
    S_full, phase = librosa.magphase(librosa.stft(
        y,
        n_fft=n_fft,
        hop_length=hop_length,
        win_length=win_length))

    # [0.1-0.5]Hz= 16-82
    # 1Hz=164
    S_full2 = np.zeros((8193, 2110))
    S_full2[16:164, :] = S_full[16:164, :]

    S_full1 = np.zeros((8193, 2110))
    S_full1[:16, :] = S_full[:16, :]
    S_full1[164:, :] = S_full[164:, :]

    # We'll compare frames using cosine similarity, and aggregate similar
    # frames by taking their (per-frequency) median value.
    S_filter = librosa.decompose.nn_filter(
        S_full1,
        aggregate=np.median,
        metric='cosine', width=200)

    # The output of the filter shouldn't be greater than the input
    S_filter = np.minimum(np.abs(S_full1), np.abs(S_filter))
    margin_i = 1
    # margin_v = 1,
    power = 2

    # Once we have the masks, simply multiply them with the input spectrogram
    # to separate the components.
    mask_i = librosa.util.softmask(
        S_filter,
        margin_i * (S_full1 - S_filter),
        power=power)

    S_background = mask_i * S_full1

    # mask_v = librosa.util.softmask(
    #     S_full1 - S_filter,
    #     margin_v * S_filter,
    #     power=power)

    # S_foreground = mask_v * S_full1

    D_harmonic, D_percussive = librosa.decompose.hpss(
        S_full2,
        kernel_size=80,
        margin=5)

    S_background = S_background+D_harmonic

    f = S_background*phase
    L = x.shape[0]
    new = librosa.istft(
        f,
        hop_length=hop_length,
        win_length=win_length,
        window='hann',
        length=L)
    z = x - new
    stats = trace[0].stats
    stats.location = 'NC'
    st = Stream([Trace(data=z, header=stats)])
    st.write(file+'-NoiseCut.mseed', format='MSEED', encoding=5, reclen=4096)

    if plotspec == 'yes':

        file2 = ('D10.DO.HH4..D.2012.080.000000-NoiseCut.mseed')
        trace2 = read(file2)
        x2 = trace2[0].data
        y2 = x2.astype(float)
        Noisereduced = librosa.stft(
            y2,
            n_fft=n_fft,
            hop_length=hop_length,
            win_length=win_length)

        fig = plt.figure(figsize=(18, 9))
        plt.subplot(3, 2, 1)
        librosa.display.specshow(
            librosa.power_to_db(np.abs(S_full)), y_axis='log', sr=sr)
        plt.title('Full spectrogram', fontsize=14)
        plt.ylabel('Frequency (Hz)', fontsize=14)
        freq = [0, 128, 512, 2048, 8000]
        labelsy = [0, 0.8, 3.2, 12.8, 50]
        plt.yticks(freq, labelsy, fontsize=14)
        plt.clim(0, 80)

        plt.subplot(3, 2, 3)
        librosa.display.specshow(
            librosa.power_to_db(np.abs(S_background)), sr=sr, y_axis='log')
        plt.ylabel('Frequency (Hz)', fontsize=14)
        plt.title('Noise spectrogram', fontsize=14)
        freq = [0, 128, 512, 2048, 8000]
        labelsy = [0, 0.8, 3.2, 12.8, 50]
        labelsx = [0, 4, 8, 12, 16, 20, 24]
        plt.yticks(freq, labelsy, fontsize=14)
        plt.clim(0, 80)

        plt.subplot(3, 2, 5)
        librosa.display.specshow(
            librosa.power_to_db(np.abs(Noisereduced)), sr=sr, y_axis='log')
        plt.ylabel('Frequency (Hz)', fontsize=14)
        plt.title('Noise reduced spectrogram', fontsize=14)
        freq = [0, 128, 512, 2048, 8000]
        labelsy = [0, 0.8, 3.2, 12.8, 50]
        labelsx = [0, 4, 8, 12, 16, 20, 24]
        plt.yticks(freq, labelsy, fontsize=14)
        labelsx = [0, 4, 8, 12, 16, 20, 24]
        plt.xticks(np.arange(0, 2110, 351.66), labelsx, fontsize=16)
        plt.clim(0, 80)

        plt.subplot(3, 2, 2)
        librosa.display.specshow(
            librosa.power_to_db(np.abs(S_full)), sr=sr, y_axis='log')
        plt.ylabel('Frequency (Hz)', fontsize=14)
        plt.title('Full spectrogram', fontsize=14)
        plt.ylim(0, 160)
        freq = [0, 32, 64, 96, 128, 160]
        labelsy = [0, 0.2, 0.4, 0.6, 0.8, 1]
        plt.yticks(freq, labelsy, fontsize=14)
        plt.clim(0, 80)

        plt.subplot(3, 2, 4)
        librosa.display.specshow(
            librosa.power_to_db(np.abs(S_background)), sr=sr, y_axis='log')
        plt.ylabel('Frequency (Hz)', fontsize=14)
        plt.title('Noise spectrogram', fontsize=14)
        plt.ylim(0, 160)
        freq = [0, 32, 64, 96, 128, 160]
        labelsy = [0, 0.2, 0.4, 0.6, 0.8, 1]
        plt.yticks(freq, labelsy, fontsize=14)
        plt.clim(0, 80)

        plt.subplot(3, 2, 6)
        librosa.display.specshow(
            librosa.power_to_db(np.abs(Noisereduced)), sr=sr, y_axis='log')
        plt.ylabel('Frequency (Hz)', fontsize=14)
        plt.title('Noise reduced spectrogram', fontsize=14)
        plt.ylim(0, 160)
        freq = [0, 32, 64, 96, 128, 160]
        labelsy = [0, 0.2, 0.4, 0.6, 0.8, 1]
        plt.yticks(freq, labelsy, fontsize=14)
        labelsx = [0, 4, 8, 12, 16, 20, 24]
        plt.xticks(np.arange(0, 2110, 351.66), labelsx, fontsize=16)
        plt.clim(0, 80)

        cb_ax = fig.add_axes([0.91, 0.12, 0.014, 0.76])
        cbar = plt.colorbar(cax=cb_ax)
        labelcl = ['0dB', '', '20dB', '', '40dB', '', '60dB', '', '80dB']
        cbar.ax.set_yticklabels(labelcl, rotation=90)
        cbar.ax.tick_params(labelsize=14)

        fig.savefig(file+'-NoiseCut.png', dpi=100)
        plt.close(fig)
