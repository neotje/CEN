import unittest
from cen_uiu.modules import dbus

class TestDBusMethods(unittest.TestCase):
    def test_get_proxy_object(self):
        self.assertIsInstance(dbus.get_proxy_object("/"), dbus.ProxyObject)
        self.assertRaises(dbus._dbus.DBusException, dbus.get_proxy_object, "/", "random.bus")

if __name__ == '__main__':
    unittest.main()