from moviepy.editor import *
import pysrt
from . import FPS

def dub(clip, text):
    srt_subs = generate_srt_from_text(text)
    def sub_gen(txt):
        return TextClip(txt, fontsize=24, color='white')
    subtitles = CompositeVideoClip(
        [clip] + [sub_gen(sub.text)
                  .set_fps(FPS)
                  .set_pos(('center', 'bottom'))
                  .set_start(sub.start.ordinal)
                  .set_duration((sub.end - sub.start).ordinal / 1000) for sub in srt_subs])
    return subtitles

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
    current_time = SUB_START_DELAY
    srt_subs = pysrt.SubRipFile()
    for p, instr in paragraphs:
        if "sub_start_time" in instr:
            current_time = instr["sub_start_time"]
        duration = len(p.split()) / SUB_WPS
        sub = pysrt.SubRipItem(
            start=int(current_time * 1000),
            end=int((current_time + duration) * 1000),
            text=p
        )
        srt_subs.append(sub)
        current_time = current_time + duration + SUB_PADDING
    return srt_subs
