import sys, os, keyword
from moviepy.editor import *
from PIL import Image
import numpy as np

EXTENSIONS = ["mov", "jpg", "mp3", "m4a", "mp4"]
RESOLUTION = (1920, 1080)

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

IMAGE_FILE_EXTENSIONS = ["png", "jpg"]
AUDIO_FILE_EXTENSIONS = ["mp3", "wav"]
VIDEO_FILE_EXTENSIONS = ["mov", "m4a"]


def set_globals_from_media(directory):
    """This is 'not advised' as it makes code very confusing.
    """
    print(">>>>>> hi")
    values = {}
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        basename, extension = os.path.splitext(name)
        extension = extension[1:]
        #if not is_python_name(basename):
        #    raise Exception(f"Not a python name: {basename}")
        print(f"{extension} vs {VIDEO_FILE_EXTENSIONS}")
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

"""
# Example Usage
original = VideoFileClip("some_video.mp4")
slide = ImageClip("some_image.jpg").set_duration(5)
resolution = (800, 600)

centered_slide = center_clip(slide, resolution)
new_clip = concatenate_videoclips([original, centered_slide])
"""

def calculate_max_resolution(clips):
    if not clips:
        raise Exception("One or more clips required")
    resolutions = [clip.size for clip in clips]
    max_width = max(res[0] for res in resolutions)
    max_height = max(res[1] for res in resolutions)
    return (max_width, max_height)

# Example Usage
# Assuming you have some clips created using moviepy
# clips = [VideoFileClip("some_video.mp4"), ImageClip("some_image.jpg")]
# print(calculate_max_resolution(clips))

def get_max_scale(resolution, target):
    width, height = resolution
    target_width, target_height = target
    if target_width - width < target_height - height:
        return target_width / width
    else:
        return target_height / height

clips = set_globals_from_media("./media")
print(clips)
globals().update(clips)

# New variables magically spawned by above.
#flowers0 = flowers_20230714.set_duration(10).set_fps(24) # .set_duration(10)
walk0 = walk_20230714.subclip(20, 80)
walk1 = walk_20230716.subclip(1, 13)
#walk2 = walk_20230718.subclip(3, 14)

#resolution = calculate_max_resolution([walk0])
""" print(f">>>>res {resolution}")
scale = get_max_scale(walk0.size, walk0.size)
print(f">>>>scl {scale}")
walk0 = walk0.resize(newsize=scale)
 """
"""
-    img = Image.open(path)
-    img.thumbnail(dimensions, Image.LANCZOS)
-    return ImageClip(np.array(img)).set_duration(duration).set_fps(24)
"""                    

result = concatenate_videoclips([
    walk0, 
    #    flowers0,
    walk1,
    #walk2
])

result.write_videofile("output.mp4", codec='libx264', fps=24)