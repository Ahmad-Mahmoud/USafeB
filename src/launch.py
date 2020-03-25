import re, os, select
from os import path
 
def locate_removable_usb()
sysblock = "/sys/block/"
sd = "sda"
removable = "/removable"
dev = "/dev/"
for char in range(ord('a'), ord('y') + 1):
    sd_list = list(sd)
    sd_list[2] = chr(char)
    sd_new = ''.join(sd_list)
    if not path.exists(sysblock+sd)
        continue
    f = open(sysblock+sd+removable)
    content = readline(f)
    if content[0] == 0
        continue
    links = os.readlink(sysblock+sd)
    regxp_search = re.search("usb", links)
    if regxp_search is None:
        continue
    #more checks should be added, in addition to optimizing the search process itself
    port_num = extract_port_num(links)
    return (port_num)
 
def extract_port_num(readlink)
    print("might need physical access to the pi for this one")
    port_num = re.findall("usb\d\/([^\/]*)", readlink)
    return port_num[0];
 
while (True):
    f = open('/proc/self/mounts')
    pollobj = select.poll() #A 'polling object'
    pollobj(f, select.POLLERR | select.POLLPRI)
    events = pollobj.poll(20*1000)
    if not events:
        continue
    else:
        port_num=get_port_num()
 
    state = (1, port_num)
 
    #if a drive new drive is detected, then
        #ensure that it's mounted properly and is working
        #exit loop and call other function