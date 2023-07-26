from mstudio import *
from mstudio.subs import *
import textwrap
import hashlib


def read_file_contents(path):
    with open(path, "r") as file:
        file_contents = file.read()
    return file_contents


# foreshadowing
def get_text_id(text):
    return hashlib.sha256(text.encode()).hexdigest()[:10]


clips = set_globals_from_media("./media")
# MAGIC: 🪄
globals().update(clips)

# CURRENT PROBS:
#
# ✔✔ flowers have no caption
# ✔✔ whale caption overflows sides
# - needs other media
# - needs mouth sounds, folded as audio
# - needs hardsubs created with our tool

# First create preamble hardsubs. It gets its own static graphic.
text = read_file_contents("apology.txt")
paragraphs = text.strip().split("\n\n")
paragraphs = [textwrap.fill(p, width=43) for p in paragraphs]
sub_rip = srt_from_paragraphs(paragraphs)
subs_clip = hardsub(sub_rip)

# New variables magically spawned by above.
tangles = tangles.set_duration(subs_clip.duration + 2).set_fps(FPS)
walk0 = walk_20230714.subclip(20, 80)
flowers0 = flowers_20230714.set_duration(10).set_fps(FPS)
walk1 = walk_20230716.subclip(1, 13)
walk2 = walk_20230718.subclip(3, 14)
whale0 = walk_20230719_0.set_duration(10).set_fps(FPS)
walk3_1 = walk_20230720_1.subclip(2, 26)

caps = caption("2023-07-14: We're walking here!")
walk0 = CompositeVideoClip(
    [walk0, caps.set_pos(("center", 55)).set_duration(walk0.duration)]
)

caps = caption("2023-07-14: DYC")
flowers0 = CompositeVideoClip(
    [flowers0, caps.set_pos(("center", 55)).set_duration(flowers0.duration)]
)

caps = caption("2023-07-16: We're walking here!")
walk1 = CompositeVideoClip(
    [walk1, caps.set_pos(("center", 55)).set_duration(walk1.duration)]
)

caps = caption("2023-07-18: We're walking here!")
walk2 = CompositeVideoClip(
    [walk2, caps.set_pos(("center", 55)).set_duration(walk2.duration)]
)

caps = caption("2023-07-19: Garbage whale.")
whale0 = CompositeVideoClip(
    [whale0, caps.set_pos(("center", 55)).set_duration(whale0.duration)]
)

caps = caption("2023-07-20: We're walking here!")
walk3_1 = CompositeVideoClip(
    [walk3_1, caps.set_pos(("center", 55)).set_duration(walk3_1.duration)]
)

result = concatenate_videoclips(
    [
        tangles,
        walk0,
        flowers0,
        walk1,
        walk2,
        whale0,
        walk3_1,
    ]
)

parent_width, parent_height = result.size
subs_width, subs_height = subs_clip.size
subs_x = (parent_width - subs_width) / 2
subs_y = parent_height - subs_height - 5
subs_clip = subs_clip.set_position((subs_x, subs_y))
result = CompositeVideoClip([result, subs_clip])

# Good to know!... Hmmm
#  mpv --geometry=1200x900 --keep-open --really-quiet output.mp4
result.write_videofile("output.mp4", **WRITEOUT_KWARGS)
