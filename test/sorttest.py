#!/usr/bin/python3

# Small test program to call the annosort.py script and sort an annotation file.
# For use with the linux operating system. May need modifiying to work with other operating system types.

import subprocess
import random

# Variables
inputfile = "GTF.gtf"
unsortedfile = "unsorted.gtf"
sortedfile = "sorted.gtf"

# Create test directory
command = "mkdir sortedfiles"
subprocess.call(command, shell=True)

# Scramble input file:  (use with small files)
print("Randomising input file")
inputobj = open("sampledata/"+inputfile)
outputobj = open("sortedfiles/"+unsortedfile,'w')
line = inputobj.readline()
while line[0]=="#":
    outputobj.write(line)
    line = inputobj.readline()
linestore = []
while line:
    linestore.append(line)
    line = inputobj.readline()
while len(linestore)>0:
    lineout = linestore.pop(random.randrange(len(linestore)))
    outputobj.write(lineout)
outputobj.close()

# Display the status of the unsorted file
print("Unsorted file status:")
command = "python3 ../annosort.py sortedfiles/"+unsortedfile+" -s"
subprocess.call(command, shell=True)

# Sort the unsorted file
print("Sorting file")
command = "python3 ../annosort.py sortedfiles/"+unsortedfile+" -o sortedfiles/"+sortedfile
subprocess.call(command, shell=True)

# Display the status of the sorted file
print("Sorted file status:")
command = "python3 ../annosort.py sortedfiles/"+sortedfile+" -s"
subprocess.call(command, shell=True)
