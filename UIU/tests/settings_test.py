import unittest
from cen_uiu.modules import settings

KEY = "unittesting"

class TestSettingsMethods(unittest.TestCase):
    def setUp(self):
        self.original = settings.getAll()

    def test_getAll(self):
        self.assertDictEqual(settings.getAll(), self.original)

    def test_setAll(self):
        self.original[KEY] = True
        settings.setAll(self.original)
        self.assertDictEqual(settings.getAll(), self.original)

    def test_get(self):
        self.assertTrue(settings.get(KEY))

    def test_set(self):
        settings.set(KEY, False)
        self.assertFalse(settings.get(KEY))


if __name__ == '__main__':
    unittest.main()