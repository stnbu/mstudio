from mstudio import *
from mstudio.subs import *

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

# New variables magically spawned by above.
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
        walk0,
        flowers0,
        walk1,
        walk2,
        whale0,
        walk3_1,
    ]
)

""" 
# Output not used for now. This slows down write-out a LOT.
result = dub(result, "x"This is the first paragraph.
Wee.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.

This is the 2nd paragraph.
Wee.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
             "x")
"""

# Good to know!... Hmmm
#  mpv --geometry=1200x900 --keep-open --really-quiet output.mp4
result.write_videofile("output.mp4", **WRITEOUT_KWARGS)
