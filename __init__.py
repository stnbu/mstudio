
DEBUG = os.getenv("DEBUG", False)
if DEBUG:
    FPS = 12
    WRITEOUT_KWARGS.update(dict(
        preset='ultrafast', fps=FPS, bitrate='500k', audio_bitrate='50k'))
else:
    FPS = 24
    WRITEOUT_KWARGS.update(dict(fps=FPS))
