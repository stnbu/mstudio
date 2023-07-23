from moviepy.editor import (ColorClip, CompositeVideoClip, TextClip,
                            concatenate_videoclips)
from pycaption import SRTReader


def create_subtitled_video(srt_filename, output_filename):
    # Read the SRT file
    with open(srt_filename, "r") as f:
        captions = SRTReader().read(f.read())

    clips = []
    for caption in captions.get_captions("en-US"):
        # Calculate the duration of this caption
        start_time = caption.start / 1000000  # convert from microseconds to seconds
        end_time = caption.end / 1000000
        duration = end_time - start_time

        # Get the text of this caption
        caption_text = " ".join(
            node.content for node in caption.nodes if node.content is not None
        )

        # Create a text clip for this caption
        txt_clip = TextClip(
            caption_text,
            fontsize=36,
            color="white",
            method="caption",
            size=(800, None),
            align="West",
        )

        # Position the text clip at the bottom of the screen
        txt_clip = txt_clip.set_position(("center", "bottom"))

        # Add a blank clip of the same duration as background
        blank_clip = ColorClip((800, 600), color=(0, 0, 0)).set_duration(duration)

        # Overlay the text clip on the blank clip
        final_clip = CompositeVideoClip([blank_clip, txt_clip]).set_duration(duration)

        # Append this clip to the list of all clips
        clips.append(final_clip)

    # Concatenate all clips into one video
    final_video = concatenate_videoclips(clips)

    # Write the result to a file
    final_video.write_videofile(output_filename, fps=24)


# Call the function
create_subtitled_video("input.srt", "output.mp4")
