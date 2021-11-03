import unittest
from cen_uiu.helpers import env

class TestEnvMethods(unittest.TestCase):
    def test_getBool(self):
        self.assertTrue(env.getBool("TEST"))
        self.assertFalse(env.getBool("TEST2"))

    def test_getStr(self):
        self.assertEqual(env.getStr("TEST"), "TRUE")
        self.assertEqual(env.getStr("TEST2"), None)

if __name__ == '__main__':
    unittest.main()