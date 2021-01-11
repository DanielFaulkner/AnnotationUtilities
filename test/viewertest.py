#!/usr/bin/python3

# Small test program to call the annoview.py script and open some sample files.
# For use with the linux operating system. May need modifiying to work with other operating system types.

import subprocess
import os
import sys

# Query file
QueryFile = "sampledata/DFAM.tsv"

# Reference file
LocalRef = "sampledata/GTF.gtf"
RefSeqName = "hg38.ncbiRefSeq.gtf"
RefSeqPath = "https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/genes/"

# Reference file selector:
print("Use included sample data (1) or use NCBI RefSeq data (2)")
usrin = input('(default 1):')
if usrin.upper()=="2":
    if os.path.exists(RefSeqName):
        RefFile = RefSeqName
    else:
        print("\nNCBI RefSeq data file not found in this directory - "+RefSeqName)
        print("\nIf you have previously downloaded the file please place a copy or link with the same filename in this directoy.")
        print("\nIf you do no have this file it can be downloaded from : "+RefSeqPath+RefSeqName)
        print("\nDownload NCBI RefSeq data (34mb) (Y) or exit (N)")
        usrin = input('(default N):')
        if usrin.upper()=="Y":
            command = "wget "+RefSeqPath+RefSeqName+".gz"
            subprocess.call(command, shell=True)
            command = "gunzip "+RefSeqName+".gz"
            subprocess.call(command, shell=True)
            RefFile = RefSeqName
        else:
            sys.exit()
else:
    RefFile = LocalRef

command = "python3 ../annoview.py "+QueryFile+" "+RefFile
subprocess.call(command, shell=True)
