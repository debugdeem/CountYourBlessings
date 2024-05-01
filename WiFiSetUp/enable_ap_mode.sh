#!/bin/bash
# Stop wpa_supplicant to free up wlan0
sudo systemctl stop wpa_supplicant@wlan0
# Restart dhcpcd to apply static IP settings for AP mode
sudo systemctl restart dhcpcd
# Start hostapd to enable AP mode
sudo systemctl start hostapd
# Start dnsmasq to enable DHCP server on wlan0
sudo systemctl start dnsmasq
