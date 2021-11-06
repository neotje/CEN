import unittest
from cen_uiu.modules import brightness

class TestBrightnessMethods(unittest.TestCase):
    def test_set_get_brightness(self):
        brightness.setBrightness(0)
        self.assertEqual(brightness.getBrightness(), 0)

        brightness.setBrightness(255)
        self.assertEqual(brightness.getBrightness(), 255)

if __name__ == '__main__':
    unittest.main()