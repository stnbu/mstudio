import pysrt
from moviepy.editor import *

from . import *


def hardsub(sub_rip):
    def get_clip(txt):
        return TextClip(txt, fontsize=48, color="white")

    clips = []
    for sub in srt_from_paragraphs(sub_rip):
        duration = sub.duration.ordinal / 1000
        start = sub.start.ordinal / 1000
        clip = get_clip(sub.text).set_start(start).set_fps(FPS).set_duration(duration)
        clips.append(clip)
    result = CompositeVideoClip(clips)
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
    # subs.save("debug.srt", encoding="utf-8")
    return subs
