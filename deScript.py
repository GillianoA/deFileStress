import os
import json
import shutil
from subprocess import PIPE, run
import sys

SCRIPT_DIR_IGNORE = ["\\deFileStress", "Downloads"]
SCRIPT_FILE_EXTENSION = ".pdf"

def getPath():
    cwd = os.getcwd()
    sourcePath = cwd.replace(SCRIPT_DIR_IGNORE[0], "")
    
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

def createDirs(source):
    newPaths = []
    for paths in source:
        dest = paths.replace(SCRIPT_DIR_IGNORE[1], "Documents")
        newPaths.append(dest)
    return newPaths

def cutAndPaste(source, dest):
    shutil.move(source, dest)

def main():
    sourcePath = getPath()
    filePaths = findAllFilePaths(sourcePath)
    destPaths = createDirs(filePaths)
    
    print(destPaths)
    for src, dest in zip(filePaths, destPaths):
        cutAndPaste(src, dest)

if __name__ == '__main__':
    main()