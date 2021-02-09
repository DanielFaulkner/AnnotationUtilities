#!/usr/bin/python3

# Small test program to call the annoatlas.py utility and add Human Protein Atlas columns to an annotation file.
# For use with the linux operating system. May need modifiying to work with other operating system types.

import subprocess
import os
import sys
import zipfile

# Variables
annotationFile = "sampledata/atlasInput.bed"    # Annotation file with a column of gene IDs
outputFile1 = "CombinedOutput1.tsv"               # Output filename
outputFile2 = "CombinedOutput2.tsv"               # Output filename
AtlasName = "proteinatlas.tsv"
AtlasPath = "https://www.proteinatlas.org/download/proteinatlas.tsv.zip"
GeneCol = 6                     # Column with gene names in the annotation file
terms1 = "9,10,50,Chromosome"   # Exact search terms or column numbers
terms2 = "RNA"                  # Search terms using regular expression

# Create test directory
command = "mkdir atlasfiles"
subprocess.call(command, shell=True)

# Atlas file locator:
print("Locating Human Protein Atlas file")
if not os.path.exists(AtlasName):
    print("\nHuman Protein Atlas data file not found in this directory - "+AtlasName)
    print("\nIf you have previously downloaded the file please place a copy or link with the same filename in this directoy.")
    print("\nIf you do no have this file it can be downloaded from : "+AtlasPath)
    print("\nDownload Human Protein Atlas tsv data file (10mb) (Y) or exit (N)")
    usrin = input('(default N):')
    if usrin.upper()=="Y":
        command = "wget "+AtlasPath
        subprocess.call(command, shell=True)
        atlaszipped = zipfile.ZipFile("proteinatlas.tsv.zip")
        atlaszipped.extractall()
    else:
        sys.exit()

# Combine columns (specified by number)
command = "python3 ../annoatlas.py "+annotationFile+" "+AtlasName+" atlasfiles/"+outputFile1+" -c "+str(GeneCol)+" -a "+terms1
subprocess.call(command, shell=True)

# Combine columns (specified by regular expression)
command = "python3 ../annoatlas.py "+annotationFile+" "+AtlasName+" atlasfiles/"+outputFile2+" -c "+str(GeneCol)+" -a "+terms2+" -r"
subprocess.call(command, shell=True)
