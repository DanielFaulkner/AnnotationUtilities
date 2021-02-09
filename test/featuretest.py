#!/usr/bin/python3

# Small test program to call the annofeat.py script and add overlapping feature columns
# For use with the linux operating system. May need modifiying to work with other operating system types.

import subprocess

# Variabl]es
queryfile = "GTF.gtf"
reffile = "GTF.gtf"
outputfile1 = "OverlappingFeatureFile.gtf"
outputfile2 = "ClosestFeatureFile.gtf"
title = "Overlapping"   # Preceding title (used with overlap option)
all = 1                 # Return all or highest priority match
margin = 0              # Extend the overlapping region by this many base pairs (used with overlap option)
sense = 1               # Order the results by sense/antisense (not used with overlap option)

# Create test directory
command = "mkdir featurefiles"
subprocess.call(command, shell=True)

# Run the annotation utility to add overlapping feature columns
# Overlapping features
command = "python3 ../annofeat.py sampledata/"+queryfile+" sampledata/"+reffile+" featurefiles/"+outputfile1+" -m "+str(margin)+" -t "+title+" -o"
if all:
    command = command+" -a"
subprocess.call(command, shell=True)

# Closest feature
command = "python3 ../annofeat.py sampledata/"+queryfile+" sampledata/"+reffile+" featurefiles/"+outputfile2
if all:
    command = command+" -a"
if sense:
    command = command+" -s"
subprocess.call(command, shell=True)
