def blacklistCheck (serial):
    #check if provided serial number is in the file
    with open("Serials.txt", 'r') as f:
        for line in f:
            if serial in line:
                return True
    return False


def blacklistAdd (serial):
    #add the provided serial number to the serials file
    f = open("Serials.txt", "a+")
    f.write("%s\n" % serial)
