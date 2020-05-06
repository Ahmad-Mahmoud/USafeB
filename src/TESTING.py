import os
import crypt

from src.crypt import Device

DIRECTORY = "C:\\Users\\folkloricye\\Downloads\\endeavouros-2019.12.22-x86_64.iso"


def main():
    computer = Device()
    computer.encrypt(DIRECTORY, 1)
    computer.decrypt()

if __name__ == '__main__':
    main()