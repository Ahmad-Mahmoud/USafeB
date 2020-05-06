import string
import random
import os
import re
import pbkdf2


# Because I needed each device to have its own key
class Device:
    def __init__(self):
        # self.rand = ''.join(random.choice(string.ascii_letters) for i in range(32))  # Rand is a random 32-byte string
        self.rand = "password"
        self.key = pbkdf2.crypt(self.rand)  # That is used to generate a key
        self.key_24 = self.key[:24]
        # self.aes = pyaes.AES(self.key_24)  # Which is used to generate an AES encryption scheme
        # self.mode = pyaes.AESModeOfOperationCTR(self.key_24)
        self.table = open('table', 'wb')

    # This function will probably be called in a loop, so file_id is supposed to be it's iterator
    # It encrypts a file into a new file then deletes the original file
    # Each device has its own table which maps the id to the original file name
    def encrypt(self, directory: string, file_id: int):
        matches = re.findall(".*/", directory)
        filename = matches[0]
        filename += "suppressed"
        filename += str(file_id)
        file_in = open(directory)
        temp = open(filename, 'wb')
        self.table.write(filename + '\n' + directory + '\n')  # This probably needs to be decrypted too
        # pyaes.encrypt_stream(self.mode, file_in, temp)
        file_in.close()
        # os.remove(directory)
        temp.close()

    # This function will also be called in a while loop, however, it will simply loop over the table
    # and decrypt everything on it, deleting the encrypted files as well
    def decrypt(self):
        files = self.table.readlines()
        dec_id = ""
        filename = ""
        decrypted = True
        for line in files:
            if decrypted:
                dec_id = line
                decrypted = False
            else:
                filename = line
                decrypted = True
            file_in = open(decrypted)
            file_out = open(filename, 'wb')
            # pyaes.decrypt_stream(self.mode, decrypted, filename)
            file_in.close()
            file_out.close()

    # def __del__(self):
    # self.table.close()
    # os.remove('table')
