#!/usr/bin/env python
# check_sigs.py - EnergyWolf 2016
# Take a file path as argument, and check it for known file
# signatures using www.filesignatures.net

# pickling the signatures file makes subsequent look ups
# significantly faster
# https://0x00sec.org/t/get-file-signature-with-python/931
#%%
import os
from urllib.request import urlopen

import pickle as Pickle

import csv

import binascii
from bs4 import BeautifulSoup
#%%
# the {} will be used to dynamically enter different ints with .format()
URL = "http://www.filesignatures.net/index.php?page=all&currentpage={}"
PATH = os.path.expanduser('./file_sigs.pickle')

signatures = [] # contains all (signatures, descriptions)
risky  = []  # contains list of risky signatures

#%%
def compile_sigs():
    """ Compile the list of file signatures """
    global signatures, PATH

    if not os.path.exists(PATH):
        for i in range(19): # 19 pages of signatures on the site
            response = urlopen(URL.format(i))
            html = response.read() # get the html as a string

            soup = BeautifulSoup(html, "lxml") # parse the source

            t_cells = soup.find_all("td", {"width": 236}) # find td elements with width=236
            for td in t_cells:
                # append (signature, extension) to signatures
                sig = str(td.get_text()).replace(' ', '').lower() # strip spaces, lowercase
                ext = str(td.find_previous_sibling("td").get_text())
                signatures.append((ext, sig))

        # pickle the signatures
        with open(PATH, 'wb') as f:
            Pickle.dump(signatures, f)

    else:
        with open(PATH, 'rb') as f:
            signatures = Pickle.load(f)
        
#%%%

def check_sig(filename):
    """ Hex dump the file and search for signatures """
    compile_sigs()
    with open(filename, 'rb') as filename:
        dump = str(binascii.hexlify(filename.read()))[2:-1]

    result = []
    possibilities = []
    flag = 0
    for  ext, sig in signatures:
        if dump.find(sig)==0:#if signature is found at offset 0
                flag = 1
                result.append((ext, sig))
                possibilities.append(ext)

    if flag ==0:
        #the file has unkown extension, hence suspicious
        return True #add to list of suspected executable files to be scanned 
    
    risky_sigs() 
    if set(possibilities)&set(risky):
        return True
    else:
        return False
 #%%%       
def risky_sigs():#reads a csv file of list of commonly known high risk extensions
    global risky
    with open('risky_file_sigs.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            risky.append(row[0])
 #%%%       
