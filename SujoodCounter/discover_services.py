# filename: discover_services.py
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
import time

class MyListener(ServiceListener):
    def __init__(self):
        self.devices = []

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            addresses = [".".join(map(str, addr)) for addr in info.parsed_addresses()]
            print(f"Service {name} added, service info: {info}")
            self.devices.append({"name": name, "address": addresses[0]})

    def remove_service(self, zeroconf, type, name):
        print(f"Service {name} removed")
        self.devices = [device for device in self.devices if device['name'] != name]

def main():
    zeroconf = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

    try:
        # Run for a specified time or wait for user input to exit
        print("Service discovery running. Press Ctrl+C to exit.")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()

if __name__ == "__main__":
    main()
