# deFileStress
Automated File Sorting Script for Windows
## Overview
`deFileStress` is a Python script designed to automate the sorting of files based on their types into specific directories. The script monitors the Downloads directory for any file modifications or creations and organizes the files into appropriate folders according to their types, such as documents, photos, music, videos, installers, archived files, and more.
## Usage Instructions
### Prerequisites
* Python 3.x installed
* `watchdog` library installed (`pip install watchdog`)
### Setup
1. Clone this repository or download the script file (`deScript.pyw`).
2. Create a folder named `deFileStress` in your Downloads directory.
3. If you want the script to run automatically on startup, create a shortcut of `deScript.pyw` and place it in the Windows Startup folder. You can find the Startup folder by pressing `Windows + R` and typing `shell:startup`.
### Execution (NOTE: This step is not necessary if the startup step was performed)
1. Run the script by double-clicking on `deScript.pyw` or executing it using a Python interpreter.
2. The script will continuously monitor the Downloads directory for file modifications or creations.
3. Files will be automatically sorted into the appropriate directories based on their types.
## Supported File Types
* Documents: `.pdf`, `.txt`, `.pptx`, `.docx`, `.xlsx`, `.xml`
* Photos: `.jpg`, `.png`, `.jpeg`, `.gif`, `.psd`
* Music: `.mp3`, `.wav`, `.flac`, `.opus`
* Videos: `.mp4`, `.flv`, `.wmv`, `.mkv`, `.avchd`, `.mov`, `.webm`, `.avi`
* Archived Files: `.zp`, `.zip`, `.rar`, `.gz`
* Installers: `.exe`, `.msp`, `.msi`, `.apk`
* Downloading Files: `.temp`, `.tmp`, `.crdownload`
## Configuration
You can customize the script by modifying the script's variables, such as file type extensions and target directory names, to suit your preferences.
``` # Edit these variables as needed
SCRIPT_DIR_IGNORE = ["\\deFileStress", "Downloads"]
SCRIPT_DIRS_IGNORE = ["deFileStress", "installers", "zips_folders", "unknown"]
# ... (Other extension lists)

# Configure these directories as needed
zipTargetPath = getTargetDir(dlPath, "zips_folders")
exeTargetPath = getTargetDir(dlPath, "installers")
# ... (Other target directories) ```
