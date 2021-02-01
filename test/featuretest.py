#!/usr/bin/python3

# Small test program to call the annofeat.py script and add overlapping feature columns
# For use with the linux operating system. May need modifiying to work with other operating system types.

import subprocess

# Variables
queryfile = "GTF.gtf"
reffile = "GTF.gtf"
outputfile = "AddedFeatureFile.gtf"
header = "Overlapping"
all = 0
margin = 0

# Create test directory
command = "mkdir featurefiles"
subprocess.call(command, shell=True)

# Run the annotation utility to add overlapping feature columns
command = "python3 ../annofeat.py sampledata/"+queryfile+" sampledata/"+reffile+" featurefiles/"+outputfile+" -m "+str(margin)+" -t "+header
if all:
    command = command+" -a"
subprocess.call(command, shell=True)
