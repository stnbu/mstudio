import os
from PIL import Image
from moviepy.editor import concatenate_videoclips, ImageClip, AudioFileClip, CompositeAudioClip
from natsort import natsorted
from muter import apply_mutes

def get_float_from_filename(filepath):
    filename = os.path.basename(filepath)
    name, _ = os.path.splitext(filename)
    return float(name)

image_dir = 'image_folder'

black_png = Image.new("RGB", (800, 600), (0, 0, 0))
black_png.save(os.path.join(image_dir, "0.0.png"))

image_files = natsorted([os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith('.png')])

clips = []
num_images = len(image_files)

for i in range(num_images):
    image_file = image_files[i]
    timestamp = get_float_from_filename(image_file)
    # Resize images using Pillow before feeding them into moviepy
    im = Image.open(image_file)
    im.thumbnail((800, 600), Image.LANCZOS)
    im.save(image_file)

    commentary_clip = apply_mutes("commentary.mov")
    
    # Determine duration of clip based on next image's timestamp
    if i < num_images - 1:
        next_timestamp = get_float_from_filename(image_files[i+1])
        duration = next_timestamp - timestamp
    else:
        # We don't know the duration of the last image, so we'll set it to the length of the longest audio clip
        jerk_clip = AudioFileClip("jerk.mp3").volumex(0.1)
        jerk_clip = jerk_clip.set_start(1043)
        duration = max(commentary_clip.duration, jerk_clip.duration)

    print(f"Creating image clip from {image_file} that begins at {timestamp} and is {duration} long")
    clips.append(ImageClip(image_file).set_start(timestamp).set_duration(duration).set_fps(24))

video = concatenate_videoclips(clips, method="compose")
audio = CompositeAudioClip([commentary_clip, jerk_clip])

final_clip = video.set_audio(audio)
final_clip.write_videofile("output.mp4", codec='libx264', fps=24)
