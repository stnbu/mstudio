from moviepy.editor import *


def caption(clip, duration=None, text=None):
    if not clip.duration:
        clip = clip.set_duration(duration)
    if not text:
        return clip
    txt_clip = (
        TextClip(
            text,
            fontsize=105,
            color="green",
            font="Arial-Rounded-MT-Bold",
            stroke_width=5,
            stroke_color="red",
        )
        .set_pos(("center", 55))
        .set_duration(clip.duration)
    )
    return CompositeVideoClip([clip, txt_clip])


walk0 = VideoFileClip("vid.mov")
flowers0 = ImageClip("flower.jpg").set_duration(1.5).set_fps(24)
whale0 = ImageClip("whale.jpg").set_duration(1.5).set_fps(24)

walk0 = caption(walk0, text="2023-07-14: We're walking here!")
flower0 = caption(flowers0, text="2023-07-19: A whale that someone has butchered.")
whale0 = caption(whale0, text="2023-07-19: A whale that someone has butchered.")

result = concatenate_videoclips(
    [
        walk0,
        flowers0,
        whale0,
    ]
)
result.write_videofile(
    "output.mp4",
    codec="libx264",
    threads=12,
    write_logfile=False,
    fps=24,
)
