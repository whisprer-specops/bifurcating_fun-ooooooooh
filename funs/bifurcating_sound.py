import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# Function to generate bifurcation data
def generate_bifurcation_data(start=2.8, end=4.0, accuracy=0.0001, reps=600, numtoplot=200):
    interval = (start, end)
    lims = np.zeros(reps)
    audio_data = []
    
    lims[0] = np.random.rand()
    for r in np.arange(interval[0], interval[1], accuracy):
        for i in range(reps - 1):
            lims[i + 1] = r * lims[i] * (1 - lims[i])
        
        # Map lims to sound frequencies
        for x in lims[reps - numtoplot:]:
            freq = 220 + x * 880  # Map x from (0, 1) to (220 Hz, 1100 Hz)
            audio_data.append(freq)
    
    return np.array(audio_data)

# Generate bifurcation data mapped to frequencies
audio_data = generate_bifurcation_data()

# Parameters for audio
sampling_rate = 44100  # 44.1 kHz standard sampling rate
duration = len(audio_data) / sampling_rate  # Duration of the audio

# Create an audio wave from the frequencies
t = np.linspace(0, duration, len(audio_data))
audio_wave = 0.5 * np.sin(2 * np.pi * audio_data * t)

# Normalize to 16-bit PCM format
audio_wave = np.int16(audio_wave / np.max(np.abs(audio_wave)) * 32767)

# Save to a WAV file
write("bifurcation_sound.wav", sampling_rate, audio_wave)

# Optional: Plot the waveform
plt.plot(audio_wave[:1000])
plt.title("Waveform of Bifurcation Plot Audio")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.show()
