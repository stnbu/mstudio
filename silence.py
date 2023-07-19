import subprocess
import shlex
import re
from moviepy.editor import AudioFileClip, CompositeAudioClip, AudioClip, concatenate_audioclips

def get_silent_interval(duration):
    return AudioClip(make_frame=lambda _: 0, duration=duration)

def get_decimal(line):
    decimals = []
    for char in line:
        if char.isdigit():
            decimals.append(char)
        elif char == '.':
            if len(decimals) > 0:
                decimals.append(char)
            else:
                raise ValueError("String does not contain exactly one decimal value.")

    if len(decimals) == 0:
        raise ValueError("String does not contain any decimal values.")
    elif decimals.count('.') > 1:
        raise ValueError("String does not contain exactly one decimal value.")
    
    decimal_str = ''.join(decimals)
    try:
        decimal_value = float(decimal_str)
        return decimal_value
    except ValueError:
        raise ValueError("String does not contain a valid decimal value.")

def get_offset_value(line):
    match = re.search(r'^[^:]*:\s*([\d.]+)', line)
    if match:
        return float(match.group(1))
    else:
        raise Exception("Was not a decimal value.")

def mute_low_noise(input_file):
    command = shlex.split(f'ffmpeg -i "{input_file}" -af silencedetect=n=-10dB:d=1 -f null - -hide_banner -nostats')
    #output = subprocess.check_output(command, stderr=subprocess.PIPE).decode('utf-8')
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, output = process.communicate()
    output = output.decode('utf-8')
    print(f"{len(output)} bytes of output")
    silence_intervals = []
    for line in output.split('\n'):
        if 'silence_start' in line:
            start_time = get_offset_value(line)
        if 'silence_end' in line:
            end_time = get_offset_value(line)
            silence_intervals.append((start_time, end_time))
    if not silence_intervals:
        raise Exception("No silence intervals detected")
    audio = AudioFileClip(input_file)
    filled_audio = audio.copy()
    position = 0.0
    clips = []
    for interval in silence_intervals:
        start, end = interval
        duration = end - start
        print(f"new audible clip: [{position}, {start}]", end = "")
        clips.append(audio.subclip(position, start))
        print(f" + new mute clip: [{start}, {end}]")
        clips.append(get_silent_interval(duration))
        position = end

    filled_audio = concatenate_audioclips(clips)
    filled_audio.fps = audio.fps
    return filled_audio
"""         x = audio.subclip(position, start_time)
        y = get_silent_interval(duration)
        filled_audio = concatenate_audioclips([filled_audio, x, y])

    filled_audio.fps = audio.fps
    return filled_audio
 """        

if __name__ == "__main__":
    clip = mute_low_noise("input.mov")
    clip.write_audiofile("silence.mp3")
