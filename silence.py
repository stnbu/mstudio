import subprocess
from moviepy.editor import AudioFileClip
from pydub import AudioSegment

def fill_silences_with_tone(input_file, tone_duration=1.0):
    # Run FFmpeg command to detect silence intervals
    command = f'ffmpeg -i "{input_file}" -af silencedetect=n=-30dB:d=1 -f null - -hide_banner -nostats -v quiet'
    output = subprocess.check_output(command, shell=True).decode('utf-8')

    # Parse FFmpeg output to extract silence intervals
    silence_intervals = []
    for line in output.split('\n'):
        if 'silence_start' in line:
            start_time = float(line.split(':')[1])
        if 'silence_end' in line:
            end_time = float(line.split(':')[1])
            silence_intervals.append((start_time, end_time))

    print(f">>>>>> {silence_intervals}")

    # Create MoviePy audio object
    audio = AudioFileClip(input_file)

    # Fill detected silence intervals with a tone
    filled_audio = audio.copy()
    for interval in silence_intervals:
        start_time = interval[0]
        end_time = interval[1]
        duration = end_time - start_time

        tone = AudioSegment.silent(duration=int(duration * 1000))
        filled_audio = filled_audio.overlay(tone, position=int(start_time * 1000))

    return filled_audio

# Example usage
input_file = 'commentary.mov'
filled_audio_clip = fill_silences_with_tone(input_file)
filled_audio_clip.write_audiofile("silence.mp3")