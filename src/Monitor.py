import subprocess
import shlex


def run_command(command):
    cntr = 0
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if b'INTERFACE DESCRIPTOR' in output :
            cntr=cntr+1
            if (b'Mass Storage' in output):
                print("Possibly Safe")
        if b'LANGID' in output :
            cntr=cntr+1
            if (b'English (United States)' in output):
                print("Possibly Safe")
        if b'Max LUN' in output :
            cntr=cntr+1
            if  (b'0' in output):
                print("Possibly Safe")
        if (cntr==3):
            break 

    rc = process.poll()
    return rc

def monitor(bus):
    run_command("tshark -i usbmon"+bus+" -V")

