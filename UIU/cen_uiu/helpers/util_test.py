import unittest
from cen_uiu.helpers import util

class TestUtilMethods(unittest.TestCase):
    def test_ping(self):
        self.assertTrue(util.ping("www.google.com"))
        self.assertFalse(util.ping("www.hopjes2.nl"))

if __name__ == '__main__':
    unittest.main()