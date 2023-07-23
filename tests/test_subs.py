from moviepy.editor import *
from mstudio import *
import unittest

class TestSubsMethods(unittest.TestCase):

    def test_simple(self):
        self.assertTrue(True)

    def test_center_clip(self):
        white_clip = ColorClip((100, 100), color=(255, 255, 255)).set_duration(0.1)
        centered = center_clip(white_clip, (200, 200))
    
        # Ensure new size matches the target resolution
        self.assertEqual(centered.size, (200, 200))
        
        # Check the four corners of the centered clip
        frame = centered.get_frame(0)

        # Upper-left corner
        self.assertEqual(frame[50, 50].tolist(), [255, 255, 255])
        
        # Upper-right corner
        self.assertEqual(frame[50, 149].tolist(), [255, 255, 255])
        
        # Lower-left corner
        self.assertEqual(frame[149, 50].tolist(), [255, 255, 255])
        
        # Lower-right corner
        self.assertEqual(frame[149, 149].tolist(), [255, 255, 255])
        