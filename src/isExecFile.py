
import os
import checkFile

def isExecFile(directory): #directory is absolute filepath of USB flash drive

    execFiles = []
    if(os.path.isdir(directory)) :
        for root, dirs, files in os.walk(directory, topdown=True):
            for filename in files:
                filepath = os.path.join(root, filename)
                if checkFile.check_sig(filepath):
                    execFiles.append([filepath, os.stat(filepath).st_size])
                    print(execFiles)
    else:
        return False #no executable files in directory
    return  execFiles #list of <possible> exexcutable files 
