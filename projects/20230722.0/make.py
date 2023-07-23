from mstudio import *
from mstudio.subs import *

clips = set_globals_from_media("./media")
# MAGIC: 🪄
globals().update(clips)

# New variables magically spawned by above.
walk0 = walk_20230714.subclip(20, 80)
flowers0 = flowers_20230714.set_duration(10).set_fps(FPS)
walk1 = walk_20230716.subclip(1, 13)
walk2 = walk_20230718.subclip(3, 14)
whale0 = walk_20230719_0.set_duration(10).set_fps(FPS)
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

# Output not used for now. This slows down write-out a LOT.
result = dub(result, """This is the first paragraph.
Wee.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.

This is the 2nd paragraph.
Wee.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
             """)

result.write_videofile("output.mp4", **WRITEOUT_KWARGS)
