import unittest
from cen_uiu.modules import bluetooth

class TestBluetoothMethods(unittest.TestCase):
    def test_get_adapter(self):
        self.assertIsInstance(bluetooth.get_adapter("hci0"), bluetooth.BluezAdapter1)

    def test_get_device(self):
        self.assertIsInstance(bluetooth.get_device("hci0", "00:00:00:00:00:00"), bluetooth.BluezDevice1)

    def test_list_devices(self):
        self.assertGreaterEqual(len(bluetooth.list_devices()), 0)

    def test_list_connected_devices(self):
        self.assertGreaterEqual(len(bluetooth.list_connected_devices()), 0)

if __name__ == '__main__':
    unittest.main()