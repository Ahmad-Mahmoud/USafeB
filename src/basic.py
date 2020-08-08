import re
import os
import subprocess
#REGEX for data extraction of USB packets
VENDOR = "(?<=idVendor).+"
PRODUCT = "(?<=iProduct).+"
ID = "(?<=idProduct).+"
SERIAL = "(?<=iSerial).+"
INTERFACE = "(?<=bInterfaceClass).+"


def dataExtract(x,bus,device):
        #extracting all connected USB devices into the system
        usbInfo = os.popen('lsusb -s '+bus+':'+device+' -v'+ ' 2>/dev/null').read()
        #Search for a specific parameter
        idLine = re.search(x,usbInfo)
        #eliminate unwanted spaces
        space = 33 - len(x)
        idClean = re.search("^.{" + str(space) + "}(.*)",idLine.group(0))
        data = (idClean.group(1))
        return data


def extractInfo(requiredInfo,bus,device):
    #extracting serial number
    if requiredInfo == "SERIAL":
         return dataExtract(SERIAL,bus,device)
    #extracting vendor ID
    elif requiredInfo == "VENDOR":
         return dataExtract(VENDOR,bus,device)
    #extracting product
    elif requiredInfo == "PRODUCT":
         return dataExtract(PRODUCT,bus,device)
    ##extracting USB ID
    elif requiredInfo == "ID":
         return dataExtract(ID,bus,device)


