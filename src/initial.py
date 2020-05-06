import re
import os
import select
from os import path
import monitor
 
 
def get_external_data():
    sysblock = "/sys/block/"
    sd = "sda"
    removable = "/removable"
    dev = "/dev/"
    port_num=""
    while(True):
        for char in range(ord('a'), ord('y') + 1):
            sd_list = list(sd)
            sd_list[2] = chr(char)
            sd_new = ''.join(sd_list)
            if not path.exists(sysblock + sd_new):
                continue
            f = open(sysblock+sd_new+removable)
            content = f.readline()
            if content[0] == 0:
                continue
            links = os.readlink(sysblock+sd_new)
            regxp_search = re.search("usb", links)
            if regxp_search is None:
                continue
            # more checks should be added, in addition to optimizing the search process itself
            port_num = extract_port_num(links)
            drive_path = dev+sd_new+'/'
            #print(port_num + ' ' + drive_path)
        if (len(port_num) != 0):
            break
    #print(port_num + ' ' + drive_path)
    data = [port_num, dev+sd_new+'/']
    return data
 
 
def extract_port_num(readlink):
    # might need physical access to the pi for this one
    port_num = re.findall("usb\d\/([^\-]*)", readlink)
    return port_num[0]
 
 
def launch():
    while (True):
        f = open('/proc/self/mounts')
        pollobj = select.poll()  # A 'polling object'
        pollobj(f, select.POLLERR | select.POLLPRI)
        events = pollobj.poll(20*1000)
        if not events:
            continue
        else:
            port_num = get_external_data()
    state = (1, port_num)
 
 
def main():
    get_external_data()
 
if __name__ == '__main__':
    main()
 
    # if a drive new drive is detected, then
    # ensure that it's mounted properly and is working
    # exit loop and call other function
