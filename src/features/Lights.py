from yeelight import discover_bulbs, Bulb
from pyHS100 import Discover

class LightStrip(Bulb):

    def __init__(self, effect='smooth', duration=1e3):
        self.ip = self.get_protocol()
        super().__init__(ip=self.ip, effect=effect, duration=duration, auto_on=True)

    def get_protocol(self):
        protocol = discover_bulbs()[0].get('ip')
        return protocol

class SmartPlugs():
    
    def __init__(self):
        self.devices = self.find_devices()

    def find_devices(self, timeout=3):
        plugs = {}
        for device in Discover.discover(timeout=timeout).values():
            plugs[device.alias] = device
        return plugs
