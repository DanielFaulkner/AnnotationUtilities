# libAnnoTabity.py
# Functions related to the conversion to an from tabulated formats
#
# By Daniel R Faulkner

# The GTF/GFF file specification has columns separated both by tabs and ';' characters.
# To convert a file into a format suitable for spreadsheet or statistical analysis a common format maybe desired

standardgtfheader = "#seqname\tsource\tfeature\tstart\tend\tscore\tstrand\tframe\tattributes"
unknownkey = "unknown"
divider = " "   # GTF Key/Value separator character. Some software outputs '=' but ' ' is standard.

# Principly designed following the GTF specification. (https://mblab.wustl.edu/GTF22.html)
# But could be adapted to support other file formats in the future.

# Inputs: Source file object, Output file object, Header option <0-None; 1-Preseve; 2-Add)
def Tabify(infileobj, outfileobj, addheader=0):
    """Convert a file into a standard tab separated file format"""
    infileobj.seek(0)
    # Treat the last comment line before the data as the header line
    line = infileobj.readline()
    header = None
    while line[0]=="#":
        if len(line.split('\t'))==9:    # Check the header has the correct number of items
            header=line
        line = infileobj.readline()
    # Write out an updated header line
    if addheader>1:
        header = standardgtfheader
    if addheader>0 and header:
        newheader=""
        # Copy the first 8 column headers unedited
        headerbase=header.split('\t')
        for i in range(0,8):
            newheader=newheader+headerbase[i]+'\t'
        # Get the remaining column headers from the first line
        attributes = line.split('\t')[8].split(';')
        for attribute in attributes:
            attribute = attribute.strip()           # Remove any preceeding spaces
            attribute.replace('=',' ')              # Account for some software using '='
            colheader = attribute.split(' ')[0]
            newheader = newheader + colheader+'\t'
        newheader = newheader.strip()+'\n'          # Replace last tab with a new line character
        outfileobj.write(newheader)
    # Process the file data
    while line:     # File pointer should still be at the first line of data
        if line[0]!='#':
            newdata = ""
            lineentries = line.split('\t')
            # Process standard tab separated columns
            for i in range(0,8):
                newdata = newdata+lineentries[i]+'\t'
            # Process attributes
            attributes = lineentries[8].split(';')
            for attribute in attributes:
                attribute = attribute.strip()
                attribute.replace('=',' ')
                value = attribute.split(' ')[-1]
                newdata = newdata+value+'\t'
            newdata = newdata.strip()+'\n'
            outfileobj.write(newdata)
        line = infileobj.readline()

# Inputs: Source file object, Output file object, Header option <0-None; 1-Preseve; 2-Add)
def deTabify(infileobj, outfileobj, addheader=0):
    """Reverses the tabulation of a file"""
    infileobj.seek(0)
    # Treat the last comment line before the data as the header line
    line = infileobj.readline()
    header = None
    while line[0]=="#":
        header=line
        line = infileobj.readline()
    # Store the column headings
    headings = None
    if header:
        header = header.strip()             # Remove any preceeding/following tabs
        if len(header.split('\t'))>8:
            headings = header.split('\t')[8:]
    # Write the header
    if addheader>1:
        newheader = standardgtfheader+'\n'
    elif addheader == 1:
        if header:
            newheader=""
            headerentries = header.split('\t')
            for i in range(0,8):
                newheader=newheader+headerentries[i]+'\t'
            newheader=newheader+"attributes\n"
        else:
            newheader=None
    else:
        newheader=None
    if newheader:
        outfileobj.write(newheader)
    # Process the data
    while line:
        if line[0]!='#':
            newdata = ""
            dataentries = line.split('\t')
            # Process required fields
            for i in range(0,8):
                newdata=newdata+dataentries[i]+'\t'
            # Process other attributes
            count = 0
            for attribute in dataentries[8:]:
                if len(headings)>=count+1:
                    key = headings[count]
                else:
                    key = unknownkey
                newdata = newdata+key+divider+attribute.strip()+'; '
                count=count+1
            newdata=newdata.strip()+'\n'
            outfileobj.write(newdata)
        line = infileobj.readline()
