import os
import json
import shutil
from subprocess import PIPE, run
import sys
import time
import zipfile

# TODO: ADD function to check if any changes were made to dir before processing
# TODO: ADD check for Dir and if directory zip tree and move to desired location
# TODO: ADD check for file extension that are not supported by the software

SCRIPT_DIR_IGNORE = ["\\deFileStress", "Downloads"]
SCRIPT_DIRS_IGNORE = ["deFileStress", "installers","zips","unknown"]
SCRIPT_DOCUMENT_EXTENSIONS = [".pdf",".txt",".pptx",".docx",".xlsx",".xml"]
SCRIPT_PHOTO_EXTENSIONS = [".jpg",".png",".jpeg",".gif",".psd"]
SCRIPT_MUSIC_EXTENSIONS = [".mp3",".wav",".flac",".opus"]
SCRIPT_VIDEO_EXTENSIONS = [".mp4",".flv",".wmv",".mkv",".avchd",".mov",".webm",".avi"]
SCRIPT_SPECIAL_EXTENSIONS = [".exe",".zip"]

# Function to get download path
def getDownloadPath():
    cwd = os.getcwd()
    dlPath = cwd.replace(SCRIPT_DIR_IGNORE[0], "")
    
    return dlPath

# Finds all folders in the downloads dir
def findAllDirPaths(source):
    dirPaths = []
    
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if SCRIPT_DIRS_IGNORE[0] in directory or SCRIPT_DIRS_IGNORE[1] in directory or SCRIPT_DIRS_IGNORE[2] in directory or SCRIPT_DIRS_IGNORE[3] in directory:
                pass
            else:
                path = os.path.join(source, directory)
                dirPaths.append(path)
        break
    return dirPaths

# zips all found folders
def zipDirs(filePath):
    fileName = os.path.basename(filePath)
    print(fileName)
    shutil.make_archive(fileName, 'zip', filePath)
    
# Finds paths to files to be transferred
def findAllFilePaths(source, extensions):
    filePaths = []
    
    for root, dirs, files in os.walk(source):
        for file in files:
            for extension in extensions:
                if file.endswith(extension):
                    path = os.path.join(source, file)
                    filePaths.append(path)
        break
    
    return filePaths

# finds to destnations for the files to be transferred to 
def findDests(source, location):
    newPaths = []
    for paths in source:
        dest = paths.replace(SCRIPT_DIR_IGNORE[1], location)
        newPaths.append(dest)
    return newPaths

# move file to new location
def cutAndPaste(source, dest):
    shutil.move(source, dest)

def main():
    while True:
        print("Processing...")
        
        dlPath = getDownloadPath()
        
        dirPaths = findAllDirPaths(dlPath)
        
        for directory in dirPaths:
            zipDirs(directory)
        
        # # Gets the file paths for all file types
        # docPaths = findAllFilePaths(dlPath, SCRIPT_DOCUMENT_EXTENSIONS)
        # photoPaths = findAllFilePaths(dlPath, SCRIPT_PHOTO_EXTENSIONS)
        # musicPaths = findAllFilePaths(dlPath, SCRIPT_MUSIC_EXTENSIONS)
        # videoPaths = findAllFilePaths(dlPath, SCRIPT_VIDEO_EXTENSIONS)
        
        # # Gets the path to be transferred to
        # docDestPaths = findDests(docPaths, "Documents")
        # photoDestPaths = findDests(photoPaths, "OneDrive\\Pictures")
        # musicDestPaths = findDests(musicPaths, "Music")
        # videoDestPaths = findDests(videoPaths, "Videos")
        
        # # Performs the transfer action for each transfer type
        # for src, dest in zip(docPaths, docDestPaths):
        #     cutAndPaste(src, dest)
        
        # for src, dest in zip(musicPaths, musicDestPaths):
        #     cutAndPaste(src, dest)
        
        # for src, dest in zip(photoPaths, photoDestPaths):
        #     cutAndPaste(src, dest)
            
        # for src, dest in zip(videoPaths, videoDestPaths):
        #     cutAndPaste(src, dest)
        
        # print("File processing complete...")
        time.sleep(6)

if __name__ == '__main__':
    main()