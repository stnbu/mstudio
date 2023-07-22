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

WPS = 3.2
START = 1.5
PADDING = 0.5

def parse_paragraphs(text):
    paragraphs = text.split("\n\n")
    subtitles = []
    instructions = {}
    for p in paragraphs:
        lines = p.split("\n")
        if lines[0].startswith("#"):
            instruction, value = lines[0][1:].split("=", 1)
            instructions[instruction.strip()] = float(value)
            subtitle_text = "\n".join(lines[1:])
        else:
            subtitle_text = p
        subtitles.append((subtitle_text, instructions))
        instructions = {}
    return subtitles

def generate_srt_from_text(text):
    paragraphs = parse_paragraphs(text)
    current_time = START
    srt_subs = pysrt.SubRipFile()
    for p, instr in paragraphs:
        if "sub_start_time" in instr:
            current_time = instr["sub_start_time"]
        duration = len(p.split()) * WPS
        sub = pysrt.SubRipItem(
            start=current_time,
            end=current_time + duration,
            text=p
        )
        srt_subs.append(sub)
        current_time = sub.end.to_time() + PADDING
    return srt_subs

def dub(clip, text):
    srt_subs = generate_srt_from_text(text)
    def sub_gen(txt):
        return TextClip(txt, fontsize=24, color='white')
    subtitles = CompositeVideoClip([clip] + [sub_gen(sub.text).set_pos(('center', 'bottom')).set_start(sub.start.to_time()).set_duration((sub.end - sub.start).to_time()) for sub in srt_subs])
    return subtitles

clips = set_globals_from_media("./media")
# MAGIC: 🪄
globals().update(clips)

# New variables magically spawned by above.
walk0 = walk_20230714.subclip(20, 80)
flowers0 = flowers_20230714.set_duration(10).set_fps(24)
walk1 = walk_20230716.subclip(1, 13)
walk2 = walk_20230718.subclip(3, 14)
whale0 = walk_20230719_0.set_duration(10).set_fps(24)
walk3_1 = walk_20230720_1.subclip(2, 26)

walk0 = caption(walk0, text="2023-07-14: We're walking here!")
flower0 = caption(flowers0, text="2023-07-14: A flower that someone has butchered.")
walk1 = caption(walk1, text="2023-07-16: We're walking here!")
walk2 = caption(walk2, text="2023-07-18: We're walking here!")
whale0 = caption(whale0, text="2023-07-19: A whale that someone has butchered.")
walk3_1 = caption(walk3_1, text="2023-07-20: We're walking here!")

result = concatenate_videoclips([
    walk0, 
    flowers0,
    walk1,
    walk2,
    whale0,
    walk3_1,
])

result.write_videofile("output.mp4", codec='libx264', fps=24)
