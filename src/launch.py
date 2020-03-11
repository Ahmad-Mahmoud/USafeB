
#This code is supposed to monitor whenever a USB drive is inserted
#It functions as an event handler
#Once a drive has been inserted, it transfers control to another function

import select, os

while (True):
    #scan fdisk entries after enabling automount on fstab
    #or monitor proc/mounts <- the best solution as Raspbian automounts drives
    #   by default in an arbitrary directory
    #or use 'watchdog' pip module

    f = open('/proc/self/mounts')
    pollobj = select.poll() #A 'polling object'
    pollobj(f, select.POLLERR | select.POLLPRI)
    pollobj.poll(None) #needs testing

    #if a drive new drive is detected, then
        #ensure that it's mounted properly and is working
        #exit loop and call other function

