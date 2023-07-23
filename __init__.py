import os
import multiprocessing

FPS = 24
WRITEOUT_KWARGS = dict(codec='libx264', threads=multiprocessing.cpu_count(), write_logfile=False, fps=FPS)

DEBUG = os.getenv("DEBUG", False)
if DEBUG:
    FPS = 12
    WRITEOUT_KWARGS.update(dict(
        preset='ultrafast', fps=FPS, bitrate='500k', audio_bitrate='50k'))
