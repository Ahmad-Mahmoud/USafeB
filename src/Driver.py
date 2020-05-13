from src.launch import get_external_data


def main():
    while (True):
        #Starting to monitor the new USB devices entering and extract the BUS number and the mounted path
        usbInfo = get_external_data()
        #Extract the serial number from the entered device
        serial = dataExtract(SERIAL)
        #Check if the device is already blacklistetd or not
        BlackListCheck(serial)
        #Monitor the descriptor packets sent from the USB and Host and detect anomalies
        monitor(usbInfo[0])
        #Check for all binary files and scan them
        vtscan(usbInfo[1])
        #IF malicious
        if (malicious == true):
            BlackListAdd(serial)
if __name__ == "__main__":
    main()

