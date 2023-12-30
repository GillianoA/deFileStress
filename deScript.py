import os
import json
import shutil
from subprocess import PIPE, run
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# TODO: ADD function to check if any changes were made to dir before processing
# TODO: ADD check for Dir and if directory zip tree and move to desired location
# TODO: ADD check for file extension that are not supported by the software
# TODO: Refactor code to remove code duplication

SCRIPT_DIR_IGNORE = ["\\deFileStress", "Downloads"]
SCRIPT_DIRS_IGNORE = ["deFileStress", "installers","zips_folders","unknown"]
SCRIPT_DOCUMENT_EXTENSIONS = [".pdf",".txt",".pptx",".docx",".xlsx",".xml"]
SCRIPT_PHOTO_EXTENSIONS = [".jpg",".png",".jpeg",".gif",".psd"]
SCRIPT_MUSIC_EXTENSIONS = [".mp3",".wav",".flac",".opus"]
SCRIPT_VIDEO_EXTENSIONS = [".mp4",".flv",".wmv",".mkv",".avchd",".mov",".webm",".avi"]
SCRIPT_ARCHIVED_EXTENSIONS = [".zp",".zip",".rar","gz"]
SCRIPT_INSTALLER_EXTENSIONS = [".exe",".msp",".msi",".apk"]

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return  # Ignore directory changes
        elif event.event_type in ['modified', 'created']:
            main()

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

# Gets the names of the files at the path specified
def getDirNames(source, dirPaths):
    dirNames = []
    
    for dirPath in dirPaths:
            dirName = dirPath.replace(source + "\\", "")
            dirNames.append(dirName)
            
    return dirNames

# zips all found folders
def getTargetDir(src, destName):
    newPath = os.path.join(src, destName)
    return newPath

# Create directory
def createDir(path):
    if not os.path.exists(path):
        os.mkdir(path)

# copies files to new location
def copyAndOverwrite(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    shutil.rmtree(source)

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
    print("Processing...")
    dlPath = os.getcwd()
    print(dlPath)
    
    # Looks for folders that arent the preprocessed ones
    dirPaths = findAllDirPaths(dlPath)
    zipPaths = findAllFilePaths(dlPath, SCRIPT_ARCHIVED_EXTENSIONS)
    exePaths = findAllFilePaths(dlPath, SCRIPT_INSTALLER_EXTENSIONS)
    
    # Gets names of files/folders to be transferred to Dir
    dirNames = getDirNames(dlPath, dirPaths)
    zipNames = getDirNames(dlPath, zipPaths)
    exeNames = getDirNames(dlPath, exePaths)
    
    # Creates the directory fpr transfers
    zipTargetPath = getTargetDir(dlPath, "zips_folders")
    createDir(zipTargetPath)
    
    exeTargetPath = getTargetDir(dlPath, "installers")
    createDir(exeTargetPath)
    
    # Moves the folders for the new directory
    for src, dest in zip(dirPaths, dirNames):
        dirDest = os.path.join(zipTargetPath, dest)
        copyAndOverwrite(src, dirDest)
    
    # Moves the zip files to the target directory
    for src, dest in zip(zipPaths, zipNames):
        dirDest = os.path.join(zipTargetPath, dest)
        cutAndPaste(src, dirDest)
    
    # transfers exe to desired directory
    for src, dest in zip(exePaths, exeNames):
        dirDest = os.path.join(exeTargetPath, dest)
        cutAndPaste(src, dirDest)
    
    # Gets the file paths for all file types
    docPaths = findAllFilePaths(dlPath, SCRIPT_DOCUMENT_EXTENSIONS)
    photoPaths = findAllFilePaths(dlPath, SCRIPT_PHOTO_EXTENSIONS)
    musicPaths = findAllFilePaths(dlPath, SCRIPT_MUSIC_EXTENSIONS)
    videoPaths = findAllFilePaths(dlPath, SCRIPT_VIDEO_EXTENSIONS)
    
    # Gets the path to be transferred to
    docDestPaths = findDests(docPaths, "Documents")
    photoDestPaths = findDests(photoPaths, "OneDrive\\Pictures")
    musicDestPaths = findDests(musicPaths, "Music")
    videoDestPaths = findDests(videoPaths, "Videos")
    
    # Performs the transfer action for each transfer type
    for src, dest in zip(docPaths, docDestPaths):
        cutAndPaste(src, dest)
    
    for src, dest in zip(musicPaths, musicDestPaths):
        cutAndPaste(src, dest)
    
    for src, dest in zip(photoPaths, photoDestPaths):
        cutAndPaste(src, dest)
        
    for src, dest in zip(videoPaths, videoDestPaths):
        cutAndPaste(src, dest)
    
    # Looks for remaining file paths
    remainingPaths = []
    for root, dirs, files in os.walk(dlPath):
        for file in files:
            path = os.path.join(dlPath, file)
            remainingPaths.append(path)
        break
    
    # Gets remaining file names
    remainingNames = getDirNames(dlPath, remainingPaths)
    
    # Create transfer Directory
    remainingTargetPath = getTargetDir(dlPath, "unknown")
    createDir(remainingTargetPath)
    
    # Moves remaining files to unknown dir
    for src, dest in zip(remainingPaths, remainingNames):
        dirDest = os.path.join(remainingTargetPath, dest)
        cutAndPaste(src, dirDest)
    
    print("File processing complete...")
    

if __name__ == '__main__':
    os.chdir('..')
    watchPath = os.getcwd()
    
    eventHandler = MyHandler()
    observer = Observer()
    observer.schedule(eventHandler, path=watchPath, recursive=True)
    
    observer.start()
    print("Running...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()