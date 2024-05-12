import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np
import os
import librosa
from scipy.signal import find_peaks
from scipy import signal

def get_peaks(freq, t, spec):
    peaks = dict()
    delta_t = 0.1
    delta_freq = 50

    for i in range(len(freq)):
        for j in range(len(t)):
            index_t = abs(t - t[j]) < delta_t
            index_freq = abs(freq - freq[i]) < delta_freq
            if not np.any(index_t) or not np.any(index_freq):
                continue
            peak_value = spec[i, j]
            is_peak = np.all(spec[index_freq][:, index_t] <= peak_value)
            if is_peak:
                peaks[freq[i]] = max(peaks.get(freq[i], 0), peak_value)

    peak_freqs = np.array(list(peaks.keys()))
    peak_values = np.array(list(peaks.values()))

    peak_indices, _ = find_peaks(peak_values)

    top_peak_freqs = peak_freqs[peak_indices[np.argsort(peak_values[peak_indices])][-3:]]

    return top_peak_freqs.tolist()

def get_max_tembr(filename):
    data, sample_rate = librosa.load(filename)

    chroma = librosa.feature.chroma_stft(y=data, sr=sample_rate)

    f0 = librosa.piptrack(y=data, sr=sample_rate, S=chroma)[0]

    max_f0 = np.argmax(f0)

    return max_f0


def min_max_freq(freq, spec, time):
    non_zero_freqs = freq[spec.sum(axis=1) != 0]  
    if len(non_zero_freqs) == 0:
        return None, None  

    max_freq = freq[np.argmax(spec.max(axis=1))]
    min_freq = freq[np.argmin(spec.max(axis=1))] 
    
    return  max_freq, min_freq

def plot_spectrogram(fs, aud, name):
    powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(aud, Fs=fs)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [s]')
    plt.savefig('output/spectrogram_' + name.split('.')[0] + '.png')
    plt.clf()
    return frequenciesFound, powerSpectrum, time

if __name__ == "__main__":
    with open('output/results.txt', "w") as file:
        for i in os.listdir('input/'):
            if i.endswith('.wav'):
                fs, aud = wav.read('input/' + i)
                f, s, t = plot_spectrogram(fs, aud, i)
                min_freq, max_freq = min_max_freq(f, s, t)
                file.write('File: ' + i + '\n')
                file.write('Min frequency: ' + str(min_freq) + '\n')
                file.write('Max frequency: ' + str(max_freq) + '\n')
                file.write('The most timbrally colored fundamental tone :' + str(get_max_tembr('input/' + i)) + '\n')
                file.write('The three most prominent peaks in the spectrogram: ' + str(get_peaks(f, t, s)) + '\n\n')
