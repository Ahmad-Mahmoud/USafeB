
import datetime
import csv
import binascii
import os

sigs = {}
risky  = set()  

#%%
#This method checks the signatures of files in the directory passed,
#outputs a list of files with suspected risky file signatures 
def isExecFile(directory): 
#directory is absolute filepath of USB flash drive
    allFiles = []
    execFiles = []
	#check if directory exists
    if(os.path.isdir(directory)) :
		#start time elapsed for performance measurement
        a = datetime.datetime.now() 
		#adds all filenames and their paths to a list  
        for root, dirs, files in os.walk(directory, topdown=True):
            for filename in files:
                filepath = os.path.join(root, filename)
                allFiles.append(filepath)
        print("#ALL FILES COUNT: ", len(allFiles))
		#reads the set of file signatures and risky signatures
        compile_sigs()
        risky_sigs()
        #checks every file if signature is in set of risky ones  
        for filepath in allFiles:
            if check_sig(filepath):
                execFiles.append((filepath, os.stat(filepath).st_size))

    if execFiles:
        b = datetime.datetime.now()
        print("Elapsed time: ", b-a)
        print("#EXECUTABLE FILES COUNT: ", len(execFiles))
        return  execFiles #list of <possible> executable files 

#%%%
#This method compares the file signature with set of risky file signatures 
def check_sig(filename):
    with open(filename, 'rb') as filename:
	#Hex dump the first 50 bytes of file
        dump = str(binascii.hexlify(filename.read(50)))[2:-1]

    possibilities = set()
    for  ext, sig in sigs.items():
        for x in sig:
		#if any signature is found at offset 0, add it to possible files
            if dump.find(x)==0:
                    possibilities.add(ext)
    #check for risky file signatures in possible files
    if possibilities&risky:
        return True
    
 #%%%    
#This method reads a csv file of list of commonly known high risk extensions into a set 
 #for ease of search and comparison 
def risky_sigs():
    global risky
    with open('risky_file_sigs.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            risky.add(row[0])

#%%
#This method reads a csv file of a table of signatures extracted from filesignatures.net
#into a dictionary for ease of search 
def compile_sigs(): 
    global sigs
    with open('sig_dictionary.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            sigs[row[0]] = row[1:]



