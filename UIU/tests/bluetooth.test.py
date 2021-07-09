from cen_uiu.modules import bluetooth, audio


def test_discoverable():
    assert bluetooth.discoverable() is True
    assert bluetooth.discoverable(False) is True


def test_set_alias():
    assert bluetooth.set_alias("Matiz") is True


def test_BluetoothInput():
    bl = audio.BluetoothInput()

    assert bl.enable() == None
    assert bl.disable() == None

if __name__ == "__main__":
    test_discoverable()
    test_set_alias()
    print("Bluetooth passed")
