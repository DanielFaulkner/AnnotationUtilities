#!/usr/bin/python3

# Small test program to call the annofilter.py script and filter a sample file using various options.
# For use with the linux operating system. May need modifiying to work with other operating system types.

import subprocess

# File to test filtering with:
TestFile = "DFAM.tsv"
# Options to test, organised as a dictionary of testnames and test arguments (adding a new entry will include those arguments in the automated test)
FilterOptions = {
	"chromosome":"--chrnames chr1",
	"chromosomeexc":"--chrnames chr1 --exclude",
	"chromosomeregex":"--chrnames \w*_alt --regex",	
	"score":"--score 500",
	"size":"--size 1000",	
	"reqregion":"--reqregion 100 300",
	"numpromoterbases":"--minpromoter 100 --defaultend 1000"
}

command = "mkdir filteredfiles"
subprocess.call(command, shell=True)

for option in FilterOptions:
	# Create the output filename
	outputname = TestFile.split('.')[0]+"filteredby"+option+"."+TestFile.split('.')[1]
	# Run the command from the terminal
	command = "python3 ../annofilter.py -i sampledata/"+TestFile+" -o filteredfiles/"+outputname+" "+FilterOptions.get(option)
	subprocess.call(command, shell=True)
