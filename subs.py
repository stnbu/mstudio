import pysrt
from moviepy.editor import *

from . import *


def hardsub(sub_rip):
    def get_clip(txt):
        color, stroke_color = FONT_COLORS_NM_EARTH
        return TextClip(
            txt,
            fontsize=65,
            color=color,
            stroke_width=3,
            stroke_color=stroke_color,
        )

    max_resolution = (0, 0)
    clips = []
    for sub in sub_rip:
        duration = sub.duration.ordinal / 1000
        start = sub.start.ordinal / 1000
        clip = get_clip(sub.text).set_start(start).set_fps(FPS).set_duration(duration)
        max_x, max_y = max_resolution
        clip_x, clip_y = clip.size
        max_x = clip_x > max_x and clip_x or max_x
        max_y = clip_y > max_y and clip_y or max_y
        max_resolution = (max_x, max_y)
        clips.append(clip)
    result = CompositeVideoClip(clips, size=max_resolution)
    return result


def srt_from_paragraphs(paragraphs):
    current_ms = SUB_START_DELAY * 1000
    subs = pysrt.SubRipFile()
    for paragraph in paragraphs:
        duration = len(paragraph.split()) / SUB_WPS * 1000
        start = int(current_ms)
        end = int(start + duration)
        sub = pysrt.SubRipItem(
            start=start,
            end=end,
            text=paragraph,
        )
        subs.append(sub)
        current_ms = end
    return subs
