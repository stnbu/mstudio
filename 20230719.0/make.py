import sys, os, keyword
from moviepy.editor import *
from PIL import Image
import numpy as np

RESOLUTION = (1920, 1080)
IMAGE_FILE_EXTENSIONS = ["png", "jpg"]
AUDIO_FILE_EXTENSIONS = ["mp3", "wav"]
VIDEO_FILE_EXTENSIONS = ["mov", "m4a"]

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ImageFileClip(ImageClip):
    def __init__(self, path):
        img = Image.open(path)
        img.thumbnail(RESOLUTION, Image.LANCZOS)
        super().__init__(np.array(img)) #.set_duration(10).set_fps(24)

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
            values[basename] = ImageFileClip(path)
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

clips = set_globals_from_media("./media")
# MAGIC: 🪄
globals().update(clips)

# New variables magically spawned by above.
flowers0 = flowers_20230714.set_duration(10).set_fps(24)
whale0 = walk_20230719_0.set_duration(10).set_fps(24)
walk0 = walk_20230714.subclip(20, 80)
walk1 = walk_20230716.subclip(1, 13)
walk2 = walk_20230718.subclip(3, 14)
walk3_1 = walk_20230720_1.subclip(2, 26)
## Save for a special occasion
#walk3_0 = walk_20230720_0_lilyshits.subclip(3, 15)


result = concatenate_videoclips([
    walk0, 
    flowers0,
    walk1,
    walk2,
    whale0,
    walk3_1,
])

result.write_videofile("output.mp4", codec='libx264', fps=24)
