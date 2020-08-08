import re
import os
import select
from os import path
import monitor
import subprocess

# This function is called when the Wireshark applet detects a new connection.
# It then searches for the new connection by iterating over devices in /sys/block and checking which ones are removable
# Then it confirms that it is a USB device and forwards its mountpoint and drive name to the next part of the code


def get_external_data():
    sysblock = "/sys/block/"
    sd = "sda"
    removable = "/removable"
    dev = "/dev/"
    port_num = ""
    while(True):
        for char in range(ord('a'), ord('y') + 1):
            sd_list = list(sd)
            sd_list[2] = chr(char)
            sd_new = ''.join(sd_list)
            if not path.exists(sysblock + sd_new):
                continue
            f = open(sysblock+sd_new+removable)
            content = f.readline()
            if content == 0:
                continue
            links = os.readlink(sysblock+sd_new)
            regxp_search = re.search("usb", links)
            if regxp_search is None:
                continue
            port_num = extract_port_num(links)
            drive_path = dev+sd_new+'/'
            if (len(port_num) != 0):
                break
        break
    result = subprocess.run(
        ['ls', '/dev/bus/usb/001/'], stdout=subprocess.PIPE)
    deviceId = result.stdout.decode("utf-8")
    deviceId = str(int(deviceId[8:11:]))
    data = [port_num, dev+sd_new+'1', deviceId]
    return data

# This function parses the string from the removable drive in order to determine its port
def extract_port_num(readlink):
    port_num = re.findall("usb\d\/([^\-]*)", readlink)
    return port_num[0]


def main():
    get_external_data()


if __name__ == '__main__':
    main()
