import os
import crypt

from src.crypt import Device

DIRECTORY = "C:\\Users\\folkloricye\\Desktop\\desktop garbage\\AtomSetup-x64.exe"


def main():
    computer = Device()
    computer.encrypt(DIRECTORY, 1)
    computer.decrypt()

if __name__ == '__main__':
    main()