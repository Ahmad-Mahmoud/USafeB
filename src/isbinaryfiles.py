from binaryornot.check import is_binary
import os

def isbinaryFiles(directory):

    filesList  = [(),()]
    binaryFiles = [(),()]
    if(os.path.isdir(directory)) :
        for root, dirs, files in os.walk(directory, topdown=True):
            for name in files:
                filepath = os.path.join(root, name)
                filesList.append([filepath , os.stat(filepath).st_size])
                if is_binary(filepath) :
                    binaryFiles.append([filepath, os.stat(filepath).st_size])
        print(binaryFiles)
    else:
        print("Directory not found")
    return filesList, binaryFiles
