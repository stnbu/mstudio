import sys
import keyword
from moviepy.editor import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def is_python_name(name):
    if keyword.iskeyword(name):
        return False
    return name.isidentifier()

import os
from moviepy.editor import VideoFileClip, AudioFileClip

EXTENSIONS = ["mov", "jpg", "mp3"]

def set_globals_from_media(directory):
    """This is 'not advised' as it makes code very confusing.
    """
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        basename, extension = os.path.splitext(name)
        if extension[1:] not in EXTENSIONS:
            continue
        if not is_python_name(basename):
            raise Exception(f"Not a python name: {basename}")
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

set_globals_from_media("./")

# New variables magically spawned by above.
flowers0 = flowers_20230714.set_duration(10)
walk0 = walk_20230714.subclip(5, 15)
walk1 = walk_20230716.subclip(5, 15)
walk2 = walk_20230718.subclip(5, 15)
