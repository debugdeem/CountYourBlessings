import re
import os

def read_wpa_config(file_path):
    """ Read and parse the wpa_supplicant.conf file to extract network blocks. """
    with open(file_path, 'r') as file:
        content = file.read()

    networks = re.findall(r'network={([^}]+)}', content, re.DOTALL)
    return networks

def write_wpa_config(file_path, networks):
    """ Write the modified network configurations back to the wpa_supplicant.conf. """
    with open(file_path, 'w') as file:
        file.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
        file.write("update_config=1\n")
        for network in networks:
            file.write("network={\n" + network + "}\n")

def manage_networks():
    config_path = '/etc/wpa_supplicant/wpa_supplicant.conf'
    networks = read_wpa_config(config_path)
    
    print("Current saved networks:")
    for idx, net in enumerate(networks, 1):
        print(f"{idx}. {net}")

    to_delete = input("Enter the numbers of the networks to delete (comma-separated): ")
    if to_delete.strip():
        indices = {int(num) - 1 for num in to_delete.split(',')}
        networks = [net for idx, net in enumerate(networks) if idx not in indices]
        write_wpa_config(config_path, networks)
        print("Updated network configurations.")
    else:
        print("No changes made.")

if __name__ == "__main__":
    manage_networks()
