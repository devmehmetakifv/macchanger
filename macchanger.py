#!/usr/bin/env python

import subprocess
import optparse
import re
import platform

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Interface to change its MAC address.")
    parser.add_option("-m","--mac",dest="new_mac",help="New MAC address to use.")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a MAC address, use --help for more info.")
    return options

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    subprocess.call(["ifconfig",interface,"up"])

#Check operating system
if platform.system() == "Linux":
    print("[+] Operating system detected: Linux. Moving on...")
else:
    print("[-] macchanger only works on Linux. Exiting...")
    exit()

#Check if user have sudo priveleges
id_result = subprocess.check_output(["id"]).decode("utf-8")
uid_string = re.search(r"uid=(\d*)", id_result)
if uid_string:
    uid = int(uid_string.group(1))
    if uid == 0:
        print("[+] User have sudo priveleges. Moving on...")
    else:
        print("[-] User doesn't have sudo priveleges. Exiting...")
        exit()

options = get_arguments()

#Parse given options to variables

interface = options.interface
new_mac = options.new_mac

#Change the MAC

change_mac(interface, new_mac)

#Check if changed

result = subprocess.check_output(["ifconfig",options.interface]).decode("utf-8")
changed_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", result)
if changed_mac.group(0) == new_mac:
    print("[+] MAC address succesfully changed!")
    subprocess.call(["ifconfig",options.interface])
else:
    print("[-] MAC address couldn't be changed.")
