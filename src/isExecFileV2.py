from urllib.request import urlopen
import datetime
import pickle as Pickle
import csv
import binascii
from bs4 import BeautifulSoup
import os


#%%
# the {} will be used to dynamically enter different ints with .format()
URL = "http://www.filesignatures.net/index.php?page=all&currentpage={}"
PATH = os.path.expanduser('./file_sigs.pickle')

signatures = [] # contains all (signatures, descriptions)
risky  = []  # contains list of risky signatures

#%%
def isExecFile(directory): #directory is absolute filepath of USB flash drive
    allFiles = []
    execFiles = []
    if(os.path.isdir(directory)) :
        for root, dirs, files in os.walk(directory, topdown=True):
            for filename in files:
                filepath = os.path.join(root, filename)
                allFiles.append(filepath)
        compile_sigs()
        risky_sigs()
        a = datetime.datetime.now()
        for filepath in allFiles:
            if check_sig(filepath):
                execFiles.append((filepath, os.stat(filepath).st_size))
    if not execFiles:
        return False #no executable files in directory
    else:
        b = datetime.datetime.now()
        print("Elapsed time: ", b-a)
        return  execFiles #list of <possible> exexcutable files 

#%%%

def check_sig(filename):
    """ Hex dump the file and search for signatures """
    with open(filename, 'rb') as filename:
        dump = str(binascii.hexlify(filename.read(10)))[2:-1]

    #result = []
    possibilities = []
    flag = 0
    for  ext, sig in signatures:
        if dump.find(sig)==0:#if signature is found at offset 0
                flag = 1
                #result.append((ext, sig))
                possibilities.append(ext)

    if flag ==0:
        #the file has unkown extension, hence suspicious
        return True #add to list of suspected executable files to be scanned 
    
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

    else:#it should jump to this section directly if pickle file exists
        with open(PATH, 'rb') as f:
            signatures = Pickle.load(f)
#%%       
            
x = isExecFile("/media/rania/C Drive/Users/Rania/Downloads")
