import re
import subprocess

usbInfo = subprocess.check_output('lsusb -s 2:10 -v', shell=True).decode('utf-8')
VENDOR = "(?<=idVendor).+"
PRODUCT = "(?<=iProduct).+"
ID = "(?<=idProduct).+"
SERIAL = "(?<=iSerial).+"
INTERFACE = "(?<=bInterfaceClass).+"


def dataExtract(x):
    idLine = re.search(x,usbInfo)
    space = 33 - len(x)
    #print (idLine.group(0))
    idClean = re.search("^.{" + str(space) + "}(.*)",idLine.group(0))
    print (idClean.group(1))

dataExtract(VENDOR)
dataExtract(PRODUCT)
dataExtract(INTERFACE)
dataExtract(ID)
dataExtract(SERIAL)

