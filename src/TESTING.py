import os
import crypt

from crypt import Device

DIRECTORY = "/mnt/8200755cbedd6f15eecd8207eba534709a01957b172d7a051b9cc4769ddbf233.bin"


def main():
    computer = Device()
    computer.encrypt(DIRECTORY, 0)
    computer.decrypt()

if __name__ == '__main__':
    main()
