#!/usr/bin/python3

# Small test program to call the annoconv.py script and convert each file in the sample data folder to every other file type.
# For use with the linux operating system. May need modifiying to work with other operating system types.

import subprocess

TestFiles = ["BED.bed","DFAM.tsv","GTF.gtf","UCSC.tsv"]
ConvertTypes = ["BED","DFAM","GTF","UCSC"]

command = "mkdir convertedfiles"
subprocess.call(command, shell=True)

for filename in TestFiles:
	for conversion in ConvertTypes:
		# Create the output filename
		if conversion == "BED":
			extension=".bed"
		elif conversion == "GTF":
			extension=".gtf"
		else:
			extension=".tsv"
		outputname = filename.split('.')[0]+"to"+conversion+extension
		# Run the command from the terminal
		command = "python3 ../annoconv.py -i sampledata/"+filename+" -o convertedfiles/"+outputname+" -c "+conversion
		subprocess.call(command, shell=True)
