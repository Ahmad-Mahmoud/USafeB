import subprocess
import shlex


def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if b'INTERFACE DESCRIPTOR' in output :
            if not (b'Mass Storage' in output):
                print("Malicious")
        if b'LANGID' in output :
            if not (b'English (United States)' in output):
                print("Malicious")
        if b'Max LUN' in output :
            if not (b'0' in output):
                print("Malicious")

    rc = process.poll()
    return rc

def monitor(bus):
    run_command("tshark -i usbmon"+bus+" -V")

if __name__ == "monitor":
    monitor()

