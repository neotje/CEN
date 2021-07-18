from cen_uiu.modules import bluetooth, audio
import dbus

d = dbus.Dictionary()
d.setdefault("test", 0)
print(d)