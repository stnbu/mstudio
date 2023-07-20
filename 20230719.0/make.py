import sys, os, keyword
from moviepy.editor import *
from PIL import Image
import numpy as np

EXTENSIONS = ["mov", "jpg", "mp3", "m4a", "mp4"]

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def is_python_name(name):
    if keyword.iskeyword(name):
        return False
    return name.isidentifier()

def set_globals_from_media(directory):
    """This is 'not advised' as it makes code very confusing.
    """
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        basename, extension = os.path.splitext(name)
        if extension[1:].lower() not in EXTENSIONS:
            continue
        if not is_python_name(basename):
            raise Exception(f"Not a python name: {basename}")
        if extension in [".jpg", ".jpeg", ".png"]:
            clip = image_to_video(path)
            globals()[basename] = clip
            continue
        try:
            clip = VideoFileClip(path)
            globals()[basename] = clip
            print(f"adding to globals: {basename} = VideoClipFile(\"{name}\")")
        except IOError:
            try:
                clip = AudioFileClip(path)
                globals()[basename] = clip
                print(f"adding to globals: {basename} = AudioClipFile(\"{name}\")")
            except IOError:
                continue

def image_to_video(path, dimensions=(800, 600), duration=0):
    img = Image.open(path)
    img.thumbnail(dimensions, Image.LANCZOS)
    return ImageClip(np.array(img)).set_duration(duration).set_fps(24)

set_globals_from_media("./media")

# New variables magically spawned by above.
flowers0 = flowers_20230714.set_duration(10)
walk0 = walk_20230714.subclip(20, 80)
walk1 = walk_20230716.subclip(1, 13).rotate(-90)
walk2 = walk_20230718.subclip(3, 14)

result = concatenate_videoclips([
    walk0, 
    flowers0,
    walk1,
    walk2
])

result.write_videofile("output.mp4", codec='libx264', fps=24)