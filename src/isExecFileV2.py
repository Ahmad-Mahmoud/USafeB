
import datetime
import csv
import binascii
import os

sigs = {}
risky  = set()  

#%%
def isExecFile(directory): #directory is absolute filepath of USB flash drive
    allFiles = []
    execFiles = []
    if(os.path.isdir(directory)) :
        a = datetime.datetime.now()
        for root, dirs, files in os.walk(directory, topdown=True):
            for filename in files:
                filepath = os.path.join(root, filename)
                allFiles.append(filepath)
        print("#all files: ", len(allFiles))
        compile_sigs()
        risky_sigs()
        
        for filepath in allFiles:
            if check_sig(filepath):
                execFiles.append((filepath, os.stat(filepath).st_size))

    if execFiles:
        b = datetime.datetime.now()
        print("Elapsed time: ", b-a)
        print("#exec files: ", len(execFiles))
        return  execFiles #list of <possible> exexcutable files 

#%%%

def check_sig(filename):
    """ Hex dump the file and search for signatures """
    with open(filename, 'rb') as filename:
        dump = str(binascii.hexlify(filename.read(10)))[2:-1]

    possibilities = set()
    for  ext, sig in sigs.items():
        for x in sig:
            if dump.find(x)==0:#if signature is found at offset 0
                    possibilities.add(ext)
    
    if possibilities&risky:
        return True
    
 #%%%       
def risky_sigs():#reads a csv file of list of commonly known high risk extensions
    global risky
    with open('risky_file_sigs.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            risky.add(row[0])

#%%
def compile_sigs():
    global sigs
    with open('sig_dictionary.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            sigs[row[0]] = row[1:]


#%%       
#example:
#execList = isExecFile("/media/user/Kingston")

#last test: 
#all files:  16637
#Elapsed time:  0:00:06.491484
#exec files:  456
