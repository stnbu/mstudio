from moviepy.editor import *
from mstudio import *
from mstudio.subs import *
import unittest


class TestSubsMethods(unittest.TestCase):
    def test_center_clip(self):
        white_clip = ColorClip((100, 100), color=(255, 255, 255)).set_duration(0.1)
        centered = center_clip(white_clip, (200, 200))
        self.assertEqual(centered.size, (200, 200))
        frame = centered.get_frame(0)
        self.assertEqual(frame[50, 50].tolist(), [255, 255, 255])
        self.assertEqual(frame[50, 149].tolist(), [255, 255, 255])
        self.assertEqual(frame[149, 50].tolist(), [255, 255, 255])
        self.assertEqual(frame[149, 149].tolist(), [255, 255, 255])

    def test_calculate_max_resolution(self):
        clip1 = ColorClip((100, 200), color=(255, 255, 255)).set_duration(0.1)
        clip2 = ColorClip((300, 100), color=(255, 255, 255)).set_duration(0.1)
        max_res = calculate_max_resolution([clip1, clip2])
        self.assertEqual(max_res, (300, 200))
