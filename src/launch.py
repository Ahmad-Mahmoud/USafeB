
#This code is supposed to monitor whenever a USB drive is inserted
#It functions as an event handler
#Once a drive has been inserted, it transfers control to another function

import select, os

while (True):
    #scan fdisk entries after enabling automount on fstab
    #or monitor proc/mounts using poll
    #or use 'watchdog' pip module

    #if a drive new drive is detected, then
        #ensure that it's mounted properly and is working
        #exit loop and call other function

