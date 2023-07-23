import os
import multiprocessing
import numpy as np
from moviepy.editor import *

SUB_WPS = 3.2
SUB_START_DELAY = 1.5
SUB_PADDING = 0.5
RESOLUTION = (1920, 1080)
IMAGE_FILE_EXTENSIONS = ["png", "jpg"]
AUDIO_FILE_EXTENSIONS = ["mp3", "wav"]
VIDEO_FILE_EXTENSIONS = ["mov", "m4a"]
FPS = 24
WRITEOUT_KWARGS = dict(codec='libx264', threads=multiprocessing.cpu_count(), write_logfile=False, fps=FPS)

DEBUG = os.getenv("DEBUG", False)
if DEBUG:
    FPS = 12
    WRITEOUT_KWARGS.update(dict(
        preset='ultrafast', fps=FPS, bitrate='500k', audio_bitrate='50k'))

def is_python_name(name):
    if keyword.iskeyword(name):
        return False
    return name.isidentifier()

def set_globals_from_media(directory):
    values = {}
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        basename, extension = os.path.splitext(name)
        extension = extension[1:]
        if extension in IMAGE_FILE_EXTENSIONS:
            values[basename] = ImageClip(path)
        elif extension in VIDEO_FILE_EXTENSIONS:
            values[basename] = VideoFileClip(path)
        elif extension in AUDIO_FILE_EXTENSIONS:
            values[basename] = AudioFileClip(path)
        else:
            continue  # not supported
    return values

def center_clip(clip, resolution):
    target_width, target_height = resolution
    clip_width, clip_height = clip.size
    pos_x = (target_width - clip_width) // 2
    pos_y = (target_height - clip_height) // 2
    centered = CompositeVideoClip([
        ColorClip(size=resolution, color=(0, 0, 0)).set_duration(clip.duration),
        clip.set_position((pos_x, pos_y))
    ])    
    return centered

def calculate_max_resolution(clips):
    if not clips:
        raise Exception("One or more clips required")
    resolutions = [clip.size for clip in clips]
    max_width = max(res[0] for res in resolutions)
    max_height = max(res[1] for res in resolutions)
    return (max_width, max_height)

def get_max_scale(resolution, target):
    width, height = resolution
    target_width, target_height = target
    if target_width - width < target_height - height:
        return target_width / width
    else:
        return target_height / height

#def sine_opacity(t):
#    return (np.sin(2 * np.pi * 3 * t) + 1) / 2  # Sine wave, 3Hz, ranged [0, 1]
    
def caption(clip, duration=None, text=None):
    if not clip.duration:
        clip = clip.set_duration(duration)
    if not text:
        return clip
    txt_clip = (TextClip(text, fontsize=105, color='green', font="Arial-Rounded-MT-Bold", 
                        stroke_width=5, stroke_color='red')
               .set_pos(('center', 55))
               .set_duration(clip.duration)) 
    # this part broke: .fx(vfx.colorx, sine_opacity))
    return CompositeVideoClip([clip, txt_clip])

def subdivide(clip):
    width, height = clip.size
    new_width = width // 2
    new_height = height // 2
    clips = [
        clip.subclip(x * new_width, (x + 1) * new_width, y * new_height, (y + 1) * new_height)
        for y in range(2)
        for x in range(2)
    ]
    for sub_clip in clips:
        sub_clip = sub_clip.set_duration(10)
    return clips

def random_concatenation(clips):
    np.random.seed(0)
    random_order = np.random.permutation(clips)
    final_clip = concatenate_videoclips(random_order, method="compose")
    return final_clip