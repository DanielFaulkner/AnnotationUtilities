# libAnnoShared
# Functions to compare an annotation file with the Human Protein Atlas dataset
#
# By Daniel R Faulkner

from lib import libAnnoShared
import re

EmptyChar = "."     # Character to use for empty fields

# TODO: Additional error checking to return an error message if an out of range column number is used

# Creates a class for addressing Human Protein Atlas files
# Usage example:
#atlasobj = atlas(open('atlasfilename'))
#HPAline = atlasobj.returndataline('GeneName')
class atlas(object):
    """Functions and operations which use the Human Protein Atlas dataset"""
    def __init__(self, atlasfileobj):
        """Perform object setup and perform any preprocessing"""
        self.fileobj = atlasfileobj
        # Store the header and store the start position for the data entries
        atlasfileobj.seek(0)
        self.header = atlasfileobj.readline()
        dataone = atlasfileobj.readline()
        self.datastart = atlasfileobj.tell()-len(dataone)
        # Determine key column numbers
        # Human Protein Atlas column titles
        geneName = "Gene"
        geneAlt = '"Gene synonym"'
        ensemblID = "Ensembl"
        # Convert to column numbers
        self.geneNameCol = libAnnoShared.columnnum(self.header,geneName)
        self.geneAltCol = libAnnoShared.columnnum(self.header,geneAlt)
        self.ensemblIDCol = libAnnoShared.columnnum(self.header,ensemblID)
    def returndataline(self, gene):
        """Return the correlating entry from the Human Protein Atlas dataset"""
        dataentry = ""
        # Process each entry looking for a match
        gene = gene.strip()
        gene = gene.upper()
        self.fileobj.seek(self.datastart)
        line = self.fileobj.readline()
        while line:
            # Prepare the fields
            fields = line.split('\t')   # Divide into seperate fields
            name = fields[self.geneNameCol].strip()
            ID = fields[self.ensemblIDCol].strip()
            synonyms=[]
            alts = fields[self.geneAltCol].split(',')
            for item in alts:
                item = item.strip()
                item = item.replace('"',"")
                synonyms.append(item.upper())
            # Perform the comparison
            if gene == name.upper():
                # Check gene name
                dataentry = line
            elif gene in synonyms:
                # Check gene synonyms
                dataentry = line
            elif gene == ID.upper():
                # Check Ensembl ID
                dataentry = line
            # Load new line, unless an entry has already been located
            line = self.fileobj.readline()
            if dataentry!="":
                line = None
        return dataentry

# Adds columns from a Human Protein Atlas file to an annotation file.
# Usage example:
#combineEntries(open('annofilename'), open('atlasfilename'), open('outputfile','w'), ['Position','Chromosome'], 0, 9):
def combineEntries(annofile, atlasfile, outputfile, atlasterms = [], regex = 0, annocol=-1):
    """Adds Human Protein Atlas information to an annotation file"""
    # Check which atlas columns to use
    atlasobj = atlas(atlasfile)
    header = atlasobj.header.strip()
    headerfields = header.split('\t')
    atlascols = []
    # If a number is passed as a search term use as a column number, and remove from list
    searchterms = []
    for item in atlasterms:
        col = -1
        try:
            col = int(item)
        except:
            stritem = item.replace('"',"")  # Remove any quotes (which may confuse matches)
            searchterms.append(stritem)
        if col>-1 and col<len(headerfields):
            if col not in atlascols:
                atlascols.append(col)
    # If a string is passed treat as an exact header string or search term
    count = 0
    if not regex:   # If the search term is an exact match include the column
        for item in headerfields:
            for search in searchterms:
                if search.upper()==item.upper():
                    if count not in atlascols:
                        atlascols.append(count)
                count = count+1
    elif regex:     # Check if the search term is a regular expression match (if regular expression flag used)
        for item in headerfields:
            if libAnnoShared.regexMatch(item,searchterms):
                if count not in atlascols:
                    atlascols.append(count)
            count = count+1
    # Add all columns if no columns specified
    if len(atlasterms)==0:
        for i in range(0,len(headerfields)):
            atlascols.append(i)
    # Process the annotation files
    type = libAnnoShared.detectFileType(annofile)
    line = annofile.readline()
    header = line
    while line[0]=="#":
        header = line
        line = annofile.readline()
    # Write out updated header line
    if header[0]=="#":  # Check this is a true header line
        newheader = header.strip()
        for item in atlascols:
            newheader=newheader+"\t"+headerfields[item]
        newheader = newheader+"\n"
        outputfile.write(newheader)
    # Add data lines
    while line:
        # Get the gene name
        if annocol>-1:
            fields = line.split('\t')
            geneName = fields[annocol]
        else:
            annotation = libAnnoShared.Annotation(line, type, header)
            geneName = annotation.repID
        # Lookup the line
        atlasline = atlasobj.returndataline(geneName)
        atlasline = atlasline.strip()
        atlasfields = atlasline.split('\t')
        numfields = len(atlasfields)
        # Output the desired fields
        outputline = line.strip()
        for item in atlascols:
            if item<numfields:
                outputline=outputline+"\t"+atlasfields[item]
            else:
                outputline=outputline+"\t"+EmptyChar
        outputline = outputline+"\n"
        outputfile.write(outputline)
        line = annofile.readline()
