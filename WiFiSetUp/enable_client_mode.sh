#!/bin/bash
# Stop the hostapd service to disable AP mode
sudo systemctl stop hostapd
# Disable the dnsmasq service to stop DHCP service on wlan0
sudo systemctl stop dnsmasq
# Restart dhcpcd to clean up configuration
sudo systemctl restart dhcpcd
# Enable wpa_supplicant to manage wlan0
sudo systemctl start wpa_supplicant@wlan0
