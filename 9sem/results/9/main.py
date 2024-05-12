import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
from math import factorial

def plot_spectrogram(fs, aud, name):
    powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(aud, Fs=fs)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [s]')
    plt.savefig('output/spectrogram_' + name + '.png')
    plt.clf()
    return powerSpectrum, frequenciesFound, time





def savitzky_golay(fs, aud, cutoff_freuency, passes=1):
    z = signal.savgol_filter(aud, 100, 3)
    b, a = signal.butter(3, cutoff_freuency / fs)
    zi = signal.lfilter_zi(b, a)
    z, _ = signal.lfilter(b, a, z, zi = zi * z[0])
    return z



def find_peaks(spec, freq, t, delta_t=0.1, delta_freq=50):
    peaks = set()
    
    t_increment = int(delta_t * len(t) / (t[-1] - t[0]))
    freq_increment = int(delta_freq * len(freq) / (freq[-1] - freq[0]))
    
    for i, freq_val in enumerate(freq):
        for j, time_val in enumerate(t):
            t_min = max(0, j - t_increment)
            t_max = min(len(t), j + t_increment + 1)
            freq_min = max(0, i - freq_increment)
            freq_max = min(len(freq), i + freq_increment + 1)
            
            is_peak = True
            for a in range(freq_min, freq_max):
                for b in range(t_min, t_max):
                    if (a != i or b != j) and spec[i, j] < spec[a, b]:
                        is_peak = False
                        break
                if not is_peak:
                    break
            
            if is_peak:
                peaks.add(time_val)
    
    return peaks
def to_pcm(y):
    return np.int16(y / np.max(np.abs(y)) * 32000)


if __name__ == "__main__":
    fs, aud = wav.read('input/sound.wav')
    aud = aud[:,0]
    plot_spectrogram(fs, aud, 'sound')
    denoised = savitzky_golay(fs, aud, 1000)
    spec, freq, time = plot_spectrogram(fs, denoised, 'denoised')
    wav.write('output/denoised.wav', fs, to_pcm(denoised))
    
    peaks = find_peaks(spec, freq, time)
    with open ('output/results.txt', 'w') as f:
        f.write("Number:" + str(len(peaks)) + '\n')
        for peak in peaks:
            f.write(str(peak) + '\n')




    
    



