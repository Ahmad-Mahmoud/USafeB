import resource
import time
#import checkFile
import blacklist
import initial
import isExecFileV2
import vtfunctions
import monitor
import basic
import crypt
import os
import psutil
import datetime

from crypt import Device

def main():
    #recording the functions time
    start = time.time()
    runcmd = datetime.datetime.now()
    #cleanup phase by unmounting any previous mounted drives
    os.system("sudo umount /mnt")
    #Monitor the descriptor packets sent from the USB and Host and detect anomalies
    print(datetime.datetime.now()- runcmd) 
    monitor.monitor("1")
    #Starting to monitor the new USB devices entering and extract the BUS number and the mounted path
    usbInfo = initial.get_external_data()
    #Extract the serial number from the entered device
    serial = basic.extractInfo("SERIAL",usbInfo[0], usbInfo[2])
    print("Device serial number is: " +serial)
    print("Device product name is: " +basic.extractInfo("PRODUCT",usbInfo[0], usbInfo[2]))
    print("Device vendor is: " +basic.extractInfo("VENDOR",usbInfo[0], usbInfo[2]))
    print("Device ID is: " + basic.extractInfo("ID",usbInfo[0], usbInfo[2]))
   
    #Check if the device is already blacklistetd or not
    check = blacklist.blacklistCheck(serial)
    if(check == True):
        print("Device is Malicious, can't proceed")
        return 0
    #Check for exectuable files on the USB drive
    #print(usbInfo[1])
    #Mounting usb device
    cmd = 'mount '+ usbInfo[1]+' /mnt'
    os.system(cmd)
    #check all suspicious file types prefacing for signature based detection phase
    execs = isExecFileV2.isExecFile("/mnt")
    if (len(execs)%2 == 0 ):
        scanningTime= ((len(execs)//2)-1)*60
    else:
        scanningTime= ((len(execs)//2))*60
    #performance measurement for scanning time
    print (scanningTime)
    #risky files handling phase
    filesToencrypt = vtfunctions.vt(execs)


    usb = []
    #Check for all binary files and scan them
    if(len(filesToencrypt) != 0):
        decide = input("Do you wish to proceed and ignore the risks?: y/n ")#
        decide = "y"
        if("y" in decide):
            i = 0
            while i < len(filesToencrypt):
                usb.append(Device(i))
                usb[i].encrypt(filesToencrypt[i], i)
                i = i+1
        #TODO: Decrypt after hardware disconnecting from host
        #needs hardware to be ready to use the GIPO ports
        #if user decided to not ignore the risks , blacklisting device procedure will work
        else:
            blacklist.blacklistAdd(serial)
    input("It's all done, Now we will assume that user has finished. Press any key to finish the simulation and restore malicious files") 
    #before ejecting the USB device , the decrypting procedure will work to restore risky files to it's original state
    for i in range (len(filesToencrypt)):
        usb[i].decrypt()
    process = psutil.Process(os.getpid())
    print(f'Time: {time.time() - start - scanningTime}') 
    #performance measurement
    print("Total memory used:" + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024) + "MB") 

if __name__ == "__main__":
    main()

