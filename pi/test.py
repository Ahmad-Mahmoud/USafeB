import subprocess
result = subprocess.run(['ls', '/dev/bus/usb/001/'], stdout=subprocess.PIPE)
#result.stdout
x = result.stdout.decode("utf-8")

print (str(int(x[8:11:])))
