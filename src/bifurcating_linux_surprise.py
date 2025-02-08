import os
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# Function to generate the bifurcation sound
def generate_bifurcation_sound():
    interval = (2.8, 4)  # start, end
    accuracy = 0.0001
    reps = 600  # number of repetitions
    numtoplot = 200
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

# Simulate a prompt for password three times
def simulate_password_prompt():
    prompt_count = 1
    while prompt_count <= 3:
        user_input = input(f"[sudo] password for {os.getlogin()}: ")
        time.sleep(3)  # Simulate sudo's pause between prompts
        prompt_count += 1

    # Instead of doing something malicious, trigger the bifurcation sound
    print("\nSomething wild is happening instead of messing with passwords!")
    generate_bifurcation_sound()

    # Display sudo's actual error message
    print("sudo: 3 incorrect password attempts")

# Execute the script
if __name__ == "__main__":
    simulate_password_prompt()
