import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.interpolate import interp1d

def generate_bifurcation_data(start=0.2, end=3.8, accuracy=0.019, reps=8500, numtoplot=200):
    interval = (start, end)
    audio_data = []
    lims = np.zeros(reps)
    
    for base_r in np.arange(interval[0], interval[1], accuracy):
        lims[0] = np.random.rand()  # random initial condition for each r
        r = base_r  # you can also add a very slight random offset here if desired
        
        for i in range(reps - 1):
            lims[i + 1] = r * lims[i] * (1 - lims[i])
        
        for x in lims[reps - numtoplot:]:
            base_freq = 150 + (x**2) * 550  # non-linear mapping to compress range
            random_shift = np.random.uniform(-0.5, 0.5)  # much reduced random shift
            freq = base_freq + random_shift
            audio_data.append(freq)
    
    return np.array(audio_data)

def smooth_data(data, window_size=20):
    return np.convolve(data, np.ones(window_size)/window_size, mode='same')

def interpolate_frequencies(freqs, factor=4):
    x_old = np.arange(len(freqs))
    x_new = np.linspace(0, len(freqs)-1, len(freqs)*factor)
    f_interp = interp1d(x_old, freqs, kind='linear')
    return f_interp(x_new)

# Generate bifurcation data mapped to frequencies
audio_data = generate_bifurcation_data()
audio_data = smooth_data(audio_data, window_size=20)
audio_data = interpolate_frequencies(audio_data, factor=4)

sampling_rate = 44100  # standard
duration = len(audio_data) / sampling_rate

# Create an audio wave from the frequencies
t = np.linspace(0, duration, len(audio_data))
audio_wave = 0.5 * np.sin(2 * np.pi * audio_data * t)

# Normalize to 16-bit PCM
audio_wave = np.int16(audio_wave / np.max(np.abs(audio_wave)) * 32767)

write("bifurcation_sound_smoothed.wav", sampling_rate, audio_wave)

plt.plot(audio_wave[:2000])
plt.title("Smoothed Bifurcation Audio")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.show()
