from moviepy.editor import *


def caption(text):
    return TextClip(
        text,
        fontsize=105,
        color="green",
        font="Arial-Rounded-MT-Bold",
        stroke_width=5,
        stroke_color="red",
    )


flower = ImageClip("flower.jpg").set_duration(1.5).set_fps(24)
cap = caption("2023-07-19: A whale that someone has butchered.")
flower = CompositeVideoClip(
    [flower, cap.set_pos(("center", 55)).set_duration(flower.duration)]
)

result = concatenate_videoclips(
    [
        flower,
    ]
)
result.write_videofile(
    "output.mp4",
    codec="libx264",
    threads=12,
    write_logfile=False,
    fps=24,
)
