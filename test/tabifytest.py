#!/usr/bin/python3

# Small test program to call the annotabify.py script and tabify/detabify a GTF file.
# For use with the linux operating system. May need modifiying to work with other operating system types.

import subprocess

# Variables
sourcefile = "GTF.gtf"
tabifyfile = "tabified.gtf"
detabfile = "detabified.gtf"
header = 1      # Include header: 0-No, 1-If present, 2-Yes

# Create test directory
command = "mkdir tabifiedfiles"
subprocess.call(command, shell=True)

# Convert all fields to tab separated columns
command = "python3 ../annotabify.py sampledata/"+sourcefile+" tabifiedfiles/"+tabifyfile+" -t "+str(header)
subprocess.call(command, shell=True)

# Restore to GTF format
command = "python3 ../annotabify.py tabifiedfiles/"+tabifyfile+" tabifiedfiles/"+detabfile+" -t "+str(header)+" -r"
subprocess.call(command, shell=True)
