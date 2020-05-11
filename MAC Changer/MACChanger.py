# Imports
import subprocess
import optparse
import re

def get_arguments():
    # Create parser
    parser = optparse.OptionParser()
    # Add command line arguments
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="mac_new", help="New wanted MAC address")
    (options, arguments) = parser.parse_args()
    # Check if arguments are set
    if not options.interface:
        # Handle error
        parser.error("[Error] No interface given, use --help for more")
    elif not options.mac_new:
        # Handle error
        parser.error("[Error] No new MAC address given, use --help for more")
    return options

# Function for changing MAC address
def change_mac(interface, mac_new):
    print(f"[Info] Changing MAC address for {interface} to {mac_new}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_new])
    subprocess.call(["ifconfig", interface, "up"])

# Obvious
def get_current_mac(interface):
    ifconfig_output = subprocess.check_output(["ifconfig", interface])
    mac_searh_output = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output.decode('utf-8'))

    if mac_searh_output:
        return mac_searh_output.group(0)
    else:
        print("[Error] Could not read MAC address")

options = get_arguments()
beginning_mac = get_current_mac(options.interface)
current_mac = get_current_mac(options.interface)
print(f"\n[Info] Current MAC address = {current_mac}")

change_mac(options.interface, options.mac_new)

# Get current MAC after changing it
current_mac = get_current_mac(options.interface)

if current_mac == options.mac_new:
    print(f"[Info] Successfully changed MAC adress from {beginning_mac} to {current_mac}")
else:
    print("[Error] Could not change MAC address, reason unknown")
