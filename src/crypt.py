import string
import random
import os
import re
from Crypto.PublicKey import RSA
from Crypto.Random import *
from Crypto.Cipher import AES


# This class is created to tie the object with its key throughout the encryption and decryption process
class Device:
    def __init__(self, i: int):
        self.key = get_random_bytes(16)
        self.cipher = AES.new(self.key, AES.MODE_GCM)
        self.name = "table" + str(i) + ".bsf"
        self.table = open(self.name, 'w')
        self.table_path = self.name
        self.table.close()

    # This function is called in a loop, so file_id is supposed to be its iterator
    # It encrypts a file into a new file then deletes the original file
    # Each object has its own table file which maps the id to the original file name
    def encrypt(self, directory: string, file_id: int):
        table = open(self.table_path, 'w')
        matches = re.findall(r".*/", directory)
        filename = matches[0]
        target_match = re.findall(r".*/(.*)", directory)
        filename += target_match[0]
        filename += ".enc"
        file_in = open(directory, 'rb')
        data = file_in.read()
        temp = open(filename, 'wb')
        table.write(filename + '\n' + directory + '\n')
        cipher_text, tag = self.cipher.encrypt_and_digest(data)
        [temp.write(x) for x in (self.cipher.nonce, tag, cipher_text)]
        file_in.close()
        os.remove(directory)
        temp.close()

    # This function will also be called in a while loop, however, it will simply loop over the table
    # and decrypt everything on it, deleting the encrypted files as well
    def decrypt(self):
        files = open(self.table_path, "r")
        data = files.read().splitlines()
        suppressed_file = ""
        filename = ""
        decrypted = True
        for line in data:
            if decrypted:
                suppressed_file = line
                decrypted = False
            else:
                filename = line
                decrypted = True
                file_in = open(suppressed_file, 'rb')
                file_out = open(filename, 'wb')
                nonce, tag, cipher_text = [
                    file_in.read(x) for x in (16, 16, -1)]
                cipher = AES.new(self.key, AES.MODE_GCM, nonce)
                data = cipher.decrypt_and_verify(cipher_text, tag)
                file_out.write(data)
                os.remove(suppressed_file)
                file_in.close()
                file_out.close()

# For the completed hardware design, the following clean-up section will be required.
    # def __del__(self):
    # self.table.close()
    # os.remove('table')
