import subprocess
import shlex
import datetime
import time
def run_command(command):
    #performance measurement
    runcmd = datetime.datetime.now()
    cntr = 0 #counter of connected devices 
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE) #executing command in background and passing its output
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        #if interface descriptor packet detected extract data
        if b'INTERFACE DESCRIPTOR' in output :
            cntr=cntr+1
            if (b'Mass Storage' in output):
                print("USB interface is \"Mass Storage\" Device (It is Possibly Safe)") 
            hid = datetime.datetime.now()
            #performance measurement
            print((hid-runcmd))
        #if language packet detected extract data
        if b'LANGID' in output :
            cntr=cntr+1
            if (b'English (United States)' in output):
                print("USB Language is \"English\" (It is Possibly Safe)")
            #performance measurement
            langid = datetime.datetime.now()
            print(langid-runcmd)
        #if # of partitions packet detected extract data
        if b'Max LUN' in output :
            cntr=cntr+1
            if  (b'0' in output):
                print("USB \"Max LUN\" is 0 so partition number is 1 (It is Possibly Safe)") 
            maxlun = datetime.datetime.now()
            #performance measurement
            print(maxlun-runcmd)
 
        if (cntr==3):
            break 

    rc = process.poll()
    return rc

def monitor(bus):
    #executing tshark and starting to monitor specific bus in the raspberry pi
    run_command("tshark -i usbmon"+bus+" -V" )

