# -----------------------------------------------------------------------------
# NoiseCut
#
# This file is part of the NoiseCut library. For licensing information see the
# accompanying file `LICENSE`.
# -----------------------------------------------------------------------------

import math
import numpy as np
import librosa
from obspy import Trace
import librosa.display
import matplotlib.pyplot as plt


# def noisecut(file, component, plotspec='no'):

def _next_pow2(n):
    return int(round(2**np.ceil(np.log2(n))))


def _valid_win_length_samples(win_length_samples, win_length, sampling_rate):
    if win_length_samples is None and win_length is None:
        # fully automatic window length
        win_length_samples = _next_pow2(120*sampling_rate)

    elif win_length_samples is None and win_length is not None:
        win_length_samples = _next_pow2(win_length*sampling_rate)

    elif win_length_samples is not None and win_length_samples is not None:
        raise ValueError(
            'Parameters win_length and win_length_samples are mutually '
            'exclusive.')
    elif win_length_samples is not None and win_length is None:
        # check win_length_samples is a power of 2
        win_length_samples = int(win_length_samples)
        if win_length_samples != _next_pow2(win_length_samples):
            raise ValueError(
                'Parameter win_length_samples must be a power of 2.')

    return win_length_samples


def noisecut(
        trace,
        ret_spectrograms=False,
        win_length_samples=None,
        win_length=None):
    '''
    Reduce noise from all the components of the OBS data using HPS noise
    reduction algorithms.

    :param win_length_samples:
        Window length in samples. Must be a power of 2. Alternatively it can be
        set with `win_length`.
    :type win_length_samples:
        int

    :param win_length:
        Window length [s]. Alternatively it can be set with
        `win_length_samples`.
    :type win_length:
        float

    :returns:
        The HPS trace and the spectrograms of the original, noise, and hps
        trace as well as an array with the frequencies.
    :return_type:
        tuple ``(hps_trace, (s_original, s_noise, s_hps, frequencies))``
    '''

    x = trace.data.astype(float)

    win_length_samples = _valid_win_length_samples(
        win_length_samples, win_length, trace.stats.sampling_rate)

    hop_length = win_length_samples // 4
    n_fft = win_length_samples

    # Compute the spectrogram amplitude and phase
    S_full, phase = librosa.magphase(librosa.stft(
        x,
        n_fft=n_fft,
        hop_length=hop_length,
        win_length=win_length_samples))

    l1 = math.floor((0.1 * win_length_samples) / trace.stats.sampling_rate)
    l2 = math.ceil((1 * win_length_samples) / trace.stats.sampling_rate)

    S_full2 = np.zeros((S_full.shape[0], S_full.shape[1]))
    S_full2[l1:l2, :] = S_full[l1:l2, :]

    S_full1 = np.zeros((S_full.shape[0], S_full.shape[1]))
    S_full1[:l1, :] = S_full[:l1, :]
    S_full1[l2:, :] = S_full[l2:, :]

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

    S_background = S_background + D_harmonic

    f = S_background * phase
    L = x.shape[0]
    new = librosa.istft(
        f,
        hop_length=hop_length,
        win_length=win_length_samples,
        window='hann',
        length=L)

    z = x - new
    stats = trace.stats
    stats.location = 'NC'

    hps_trace = Trace(data=z, header=stats)

    if ret_spectrograms:
        # S_hps = librosa.stft(
        #     z,
        #     n_fft=n_fft,
        #     hop_length=hop_length,
        #     win_length=win_length_samples)

        S_hps = S_full - S_background

        df = trace.stats.sampling_rate/win_length_samples
        frequencies = np.arange(S_hps.shape[0]) * df
        times = np.arange(S_hps.shape[1]) * hop_length

        return hps_trace, (S_full, S_background, S_hps, frequencies, times)
    else:
        return hps_trace


def power_to_db(spec):
    # TODO return spec
    return spec
def power_to_db(S, amin=1e-16, top_db=80.0):
    """Convert a power-spectrogram (magnitude squared) to decibel (dB) units.
    Computes the scaling ``10 * log10(S / max(S))`` in a numerically
    stable way.
    """
    def _tf_log10(x):
        numerator = tf.math.log(x)
        denominator = tf.math.log(tf.constant(10, dtype=numerator.dtype))
        return numerator / denominator
    
    # Scale magnitude relative to maximum value in S. Zeros in the output 
    # correspond to positions where S == ref.
    ref = tf.reduce_max(S)

    log_spec = 10.0 * _tf_log10(tf.maximum(amin, S))
    log_spec -= 10.0 * _tf_log10(tf.maximum(amin, ref))

    log_spec = tf.maximum(log_spec, tf.reduce_max(log_spec) - top_db)

    return log_spec


def plot_noisecut_spectrograms(
        S_full, S_background, S_hps, frequencies, times):

    fig = plt.figure(figsize=(16, 9))
    axes = plt.subplot(3, 1, 3)

    plt.subplot(3, 1, 1)
    axes.pcolormesh(times, frequencies, power_to_db(np.abs(S_full)))
    plt.title('Full spectrogram', fontsize=14)
    plt.ylabel('Frequency (Hz)', fontsize=14)
    plt.colorbar()
    
    plt.subplot(3, 1, 2)
    axes.pcolormesh(times, frequencies, power_to_db(np.abs(S_background)))
    plt.ylabel('Frequency (Hz)', fontsize=14)
    plt.title('Noise spectrogram', fontsize=14)
    plt.colorbar()
    
    plt.subplot(3, 1, 3)
    axes.pcolormesh(times, frequencies, power_to_db(np.abs(S_hps)))
    plt.ylabel('Frequency (Hz)', fontsize=14)
    plt.title('Nenoised spectrogram', fontsize=14)
    plt.colorbar()
    
    plt.close(fig)

hps_trace, spectrograms = noisecut(...)
plot_noisecut_spectrograms(*spectrograms)