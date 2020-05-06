import checkFile
import blacklist
import initial
import isExecFile
import vtfunctions
import monitor
import basic


def main():
    
    #Monitor the descriptor packets sent from the USB and Host and detect anomalies
    #monitor.monitor("2")
    #Starting to monitor the new USB devices entering and extract the BUS number and the mounted path
    #usbInfo = initial.get_external_data()
    #Extract the serial number from the entered device
    #x="65" #Awaiting ismail device ID
    #serial = basic.extractInfo("SERIAL",usbInfo[0],x)
    ##print(serial)
    #Check if the device is already blacklistetd or not
    ##print(blacklist.blacklistCheck(serial))
    #Check for exectuable files on the USB drive
    #print(usbInfo[1])
    print(isExecFile.isExecFile("/mnt"))
    
    #Check for all binary files and scan them
    #vtscan(usbInfo[1])
    #IF malicious
    #if (malicious == true):
    #   BlackListAdd(serial)
if __name__ == "__main__":
    main()

