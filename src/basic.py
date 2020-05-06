import re
import subprocess

VENDOR = "(?<=idVendor).+"
PRODUCT = "(?<=iProduct).+"
ID = "(?<=idProduct).+"
SERIAL = "(?<=iSerial).+"
INTERFACE = "(?<=bInterfaceClass).+"


def dataExtract(x,bus,device):
    usbInfo = subprocess.check_output('lsusb -s '+bus+':'+device+' -v', shell=True).decode('utf-8')
    idLine = re.search(x,usbInfo)
    space = 33 - len(x)
    #print (idLine.group(0))
    idClean = re.search("^.{" + str(space) + "}(.*)",idLine.group(0))
    data = (idClean.group(1))
    return data

def extractInfo(requiredInfo,bus,device):
    if requiredInfo == "SERIAL":
         return dataExtract(SERIAL,bus,device)
    elif requiredInfo == "VENDOR":
         return dataExtract(VENDOR,bus,device)
    elif requiredInfo == "PRODUCT":
         return dataExtract(PRODCUT,bus,device)
    elif requiredInfo == "ID":
         return dataExtract(ID,bus,device)


