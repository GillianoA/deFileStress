import os
import json
import shutil
from subprocess import PIPE, run
import sys

SCRIPT_DIR_IGNORE = "\\deFileStress"
SCRIPT_FILE_EXTENSION = ".pdf"

def getPath():
    cwd = os.getcwd()
    sourcePath = cwd.replace(SCRIPT_DIR_IGNORE, "")
    
    return sourcePath

def findAllFilePaths(source):
    filePaths = []
    
    for root, dirs, files in os.walk(source):
        for file in files:
            if file.endswith(SCRIPT_FILE_EXTENSION):
                path = os.path.join(source, file)
                filePaths.append(path)
                
        break
    
    return filePaths

def main():
    sourcePath = getPath()
    filePaths = findAllFilePaths(sourcePath)
    
    print(filePaths)

if __name__ == '__main__':
    main()