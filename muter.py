import os
from moviepy.editor import AudioFileClip, concatenate_audioclips
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np

def apply_mutes(audio_file_path):
    mutes_path = os.path.splitext(audio_file_path)[0] + ".mutes"
    mute_intervals = parse_intervals(mutes_path)

    # Load the audio file
    audio = AudioFileClip(audio_file_path)

    # Make sure the intervals are sorted
    mute_intervals.sort()

    clips = []
    last_end = 0
    for start, end in mute_intervals:
        # Include non-muted parts
        if start > last_end:
            clips.append(audio.subclip(last_end, start))
        
        # Create a silent audio clip for the mute interval and add it
        duration = end - start
        silence = AudioArrayClip(np.zeros((int(duration * audio.fps), 2)), fps=audio.fps)
        clips.append(silence)
        
        last_end = end

    # Append any remaining non-muted part
    if last_end < audio.duration:
        clips.append(audio.subclip(last_end, audio.duration))

    # Concatenate everything
    final_audio = concatenate_audioclips(clips)

    return final_audio

######

import re

def parse_intervals(file_path):
    mute_intervals = []

    with open(file_path, 'r') as f:
        for line in f:
            # Use regex to match the format mute(<start>, <end>)
            match = re.search(r'mute\((.*), (.*)\)', line)
            if match:
                start, end = float(match.group(1)), float(match.group(2))
                mute_intervals.append((start, end))

    return mute_intervals
