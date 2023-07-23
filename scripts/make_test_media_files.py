import os

import numpy as np
from moviepy.editor import *
from PIL import Image
from scipy.io.wavfile import write


# Function to generate a tone
def generate_tone(frequency, duration, volume, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * t * 2 * np.pi) * volume
    return tone


# Save tone as a wav file
def save_tone(filename, tone, sample_rate=44100):
    write(filename, sample_rate, tone)


# Create a temporary wav file for the MOV
save_tone("temp.wav", generate_tone(440, 10, 0.1))
audio_mov = AudioFileClip("temp.wav")
video_mov = (
    ColorClip((640, 480), col=(0, 0, 0), duration=10).set_duration(10).set_fps(24)
)  # Specify fps here
video_mov.set_audio(audio_mov)
video_mov.write_videofile("./commentary.mov", codec="libx264")

# Create a temporary wav file for the MP3 and then convert it to MP3
save_tone("temp.wav", generate_tone(880, 3, 0.1))
audio_mp3 = AudioFileClip("temp.wav")
audio_mp3.write_audiofile("./jerk.mp3")

# Create PNG image file
image_folder = "./image_folder"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

img = Image.new("RGB", (900, 900), color="green")
img.save("./image_folder/6.0.png")

# Clean up temporary wav file
os.remove("temp.wav")
