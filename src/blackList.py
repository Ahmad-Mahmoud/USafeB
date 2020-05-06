def blacklistCheck (serial):
    flag = 0
    with open("Serials.txt", 'r') as f:
        for line in f:
            if serial in line:
                return True
    return False


def blacklistAdd (serial):
    f = open("Serials.txt", "a+")
    f.write("%s\n" % serial)
