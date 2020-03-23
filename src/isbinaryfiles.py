from binaryornot.check import is_binary
import os

def isbinaryFiles(directory):

    Files  = []
    binaryFiles = []
    if(os.path.isdir(directory)) :
        for root, dirs, files in os.walk(directory, topdown=True):
            for name in files:
                Files.append(os.path.join(root, name))
                if is_binary(os.path.join(root, name)) :
                    binaryFiles.append(os.path.join(root, name))
        print(binaryFiles)
    else:
        print("Directory not found")
    return Files, binaryFiles