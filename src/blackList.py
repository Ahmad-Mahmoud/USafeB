def BlackListCheck (serial):
    flag = 0
    with open("Serials.txt", 'r') as f:
        for line in f:
            box = line
            box = int(box)
            if (box == serial):
                flag = 1
    if (flag == 0):
        BlackListAdd(serial)
    return True


def BlackListAdd (serial):
    f = open("Serials.txt", "a+")
    f.write("%d\n" % serial)
    return True
