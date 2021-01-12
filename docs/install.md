# Installation

## Requirements:

The annotation utilities are written in, and require, a recent version of Python (version 3).

## Instructions:

The utilities do not require installing. Provided they are downloaded and are in a directory along with the lib directory they can be run from that location using python (ie. python3 /path/to/utility.py).

To make use easier for Linux based operating systems an install script is provided which will configure the utilities so they can be started without the python command (ie. ./path/to/utility.py) and you will be prompted if it is possible to update your user settings to make the application available without typing the full file path (ie. utility.py).

To start the install script from a terminal enter:
python3 install.py

No changes will be made to your user account settings without confirmation.


## Uninstallation:

To uninstall simply delete the directory containing these utilites. If you have used the installer to make the utilites available without typing in the file path you will need to edit the ~/.bashrc file to comment out or remove the added line (indicated by a preceeding identifying comment).
