"""
org.bluez.AgentManager1 interface

https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/agent-api.txt
"""
import dbus
import dbus.service

from cen_uiu.helpers import bus


class BluezAgentManager1(bus.Object):
    def __init__(self, conn: dbus.Bus):
        super().__init__(conn=conn, object_path="/org/bluez")

    @dbus.service.method("org.bluez.AgentManager1", in_signature="os")
    def RegisterAgent(self, agent: dbus.ObjectPath, capability: dbus.String):
        pass

    @dbus.service.method("org.bluez.AgentManager1", in_signature="o")
    def UnregisterAgent(self, agent: dbus.ObjectPath):
        pass

    @dbus.service.method("org.bluez.AgentManager1", in_signature="o")
    def RequestDefaultAgent(self, agent: dbus.ObjectPath):
        pass
