import re
from glob import glob

import numpy as np
from moviepy.editor import *
from moviepy.editor import (AudioFileClip, CompositeAudioClip, ImageClip,
                            concatenate_videoclips)
# import PIL
from PIL import Image


def make_images_clip(images_dir, length=0):
    # Get a list of image files in the directory
    image_files = sorted(glob(os.path.join(images_dir, "*.*.*")))
    timestamps = []
    clips = []

    # Extract timestamps from image file names
    for file_name in image_files:
        timestamp = float(os.path.basename(file_name).split(".")[0])
        timestamps.append(timestamp)

    # Determine the total clip length
    total_length = max(timestamps[-1], length)

    # Create a black video clip
    video = ColorClip((800, 600), duration=total_length, col=(0, 0, 0))

    # Iterate over the timestamps and corresponding images
    for timestamp, image_path in zip(timestamps, image_files):
        img = Image.open(image_path)
        img.thumbnail((800, 600))
        image = ImageClip(np.array(img)).set_duration(total_length - timestamp)

        # Set the image as the video content from the timestamp until the next timestamp
        video = CompositeVideoClip([video, image.set_start(timestamp)])

    # If the last image is not until the end of the clip, set it as the video content
    img = Image.open(image_files[-1])
    img.thumbnail((800, 600))
    last_image = ImageClip(np.array(img))
    video = CompositeVideoClip(
        [video, last_image.set_start(timestamps[-1])]
    ).set_duration(total_length)
    return video


if __name__ == "__main__":
    video = make_images_clip("images_dir")
    video.set_duration(2000)
    video.write_videofile("slide.mp4", codec="libx264", fps=24)
