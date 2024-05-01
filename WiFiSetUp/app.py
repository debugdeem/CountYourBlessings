from flask import Flask, render_template, request, redirect, jsonify
import subprocess
import time
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ssid = request.form.get('ssid')
        if ssid == "hidden":
            ssid = request.form.get('hidden_ssid')
        password = request.form.get('password')
        # Toggle client mode
        toggle_mode('client')
        success = configure_wifi(ssid, password)
        if success:
            return 'Wi-Fi configured successfully!'
        else:
            return render_template('fail.html', message='Failed to connect to Wi-Fi. Please check your credentials and try again.')
    else:
        # Ensure AP mode is disabled when accessing the index page
        toggle_mode('ap')
    networks = scan_wifi_networks()
    return render_template('index.html', networks=networks)

def toggle_mode(mode):
    if mode == 'client':
        # Stop hostapd and dnsmasq to free up the WLAN interface
        subprocess.run(['sudo', 'systemctl', 'stop', 'hostapd', 'dnsmasq'], check=True)
        # Ensure wpa_supplicant is active to manage WLAN in client mode
        subprocess.run(['sudo', 'systemctl', 'start', 'wpa_supplicant'], check=True)
    elif mode == 'ap':
        # Stop wpa_supplicant to free up the WLAN interface for AP mode
        subprocess.run(['sudo', 'systemctl', 'stop', 'wpa_supplicant'], check=True)
        # Start hostapd and dnsmasq to enable AP mode
        subprocess.run(['sudo', 'systemctl', 'start', 'hostapd', 'dnsmasq'], check=True)

def scan_wifi_networks():
    try:
        result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True)
        return parse_networks(result.stdout)
    except subprocess.CalledProcessError:
        logging.error("Failed to scan networks")
        return []

def parse_networks(iwlist_output):
    networks = []
    for line in iwlist_output.split('\n'):
        if "ESSID:" in line:
            ssid = line.split('"')[1]
            if ssid:
                networks.append(ssid)
    return networks

def configure_wifi(ssid, password):
    config_commands = [
        f'sudo iwconfig wlan0 essid {ssid} key s:{password}',
        'sudo dhclient wlan0 -v'
    ]
    try:
        for command in config_commands:
            subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to connect to {ssid}: {str(e)}")
        return False

@app.route('/switch-to-ap', methods=['POST'])
def switch_to_ap():
    toggle_mode('ap')
    return jsonify({'status': 'Switched to Access Point mode'})

@app.route('/connect-to-wifi', methods=['POST'])
def connect_to_wifi():
    ssid = request.form.get('ssid')
    password = request.form.get('password')
    toggle_mode('client')
    if configure_wifi(ssid, password):
        return jsonify({'status': 'Connected to WiFi successfully'})
    else:
        return jsonify({'status': 'Failed to connect to WiFi'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020)