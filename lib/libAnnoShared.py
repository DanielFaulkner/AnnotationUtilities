# libAnnoShared
# Code shared between multiple different utilties that interact with annotation files
#
# By Daniel R Faulkner

import re

# Return the column number from a name in the header.
# Note: This is case sensitive. An advancement in future maybe to return a dictionary with all header columns.
def columnnum(header, name, default=-1):
    """Returns the column number matching the input string when provided with a tab separated header."""
    column = default
    count = 0
    for item in header.split("\t"):
        if item.strip() == name.strip():
            column = count
        else:
            count = count +1
    return column

# Checks the query against a list of regular expressions.
# INPUT: A string to examine. A list of regular expression search terms.
# OUTPUT: Returns 0 if no match is found or 1 if one of the regular expressions matches
def regexMatch(query, list):
    """Loops through a list of regular expressions until a match is found"""
    # Loop through the list looking for a match
    passed = 0
    for name in list:
        try:
            regname = re.compile(name)
        except:
            raise Exception(name+" is not a compatible regular expression.")
        if regname.search(query):
            passed=1
            break
    return passed

# Creates an object for an entry in an annotation file and applies basic conversions to make the data consistant
# INPUT: Line from annotation file, the input file format and the header line where available.
# NOTE: Scores are stored as integers. This could be changed to a float for greater accuracy. (Supported by DFAM and GTF)
class Annotation(object):
    """Parses an annotation line and stores key values in a common structure"""
    def __init__(self, line, type, header="", NullString=".", NullInt=-1):
        self.line = line
        self.type = type
        self.header = header
        self.error = None
        self.NullString = NullString
        self.NullInt = NullInt
        if type=="BED":
            self.parseBed()
        elif type=="UCSC":
            self.parseUcsc()
        elif type=="DFAM":
            self.parseDfam()
        elif type=="GTF":
            self.parseGtf()
        else:
            self.error = "Type unsupported "+self.type
    def parseBed(self):
        fields = self.line.split('\t')
        # Variables for external use:
        self.repName = fields[3].strip()
        self.repSize = self.NullInt
        self.chrName = fields[0].strip()
        self.chrSize = self.NullInt
        self.score = int(fields[4])
        self.strand = fields[5].strip()
        self.alignStart = int(fields[1])
        self.alignEnd = int(fields[2])
        self.matchStart = self.NullInt
        self.matchEnd = self.NullInt
        self.repID = self.NullString
    def parseUcsc(self):
        fields = self.line.split('\t')
        # Conversions
        if fields[columnnum(self.header, "strand")] == "-":
            repstart = int(fields[columnnum(self.header, "repLeft")])
            repsize = int(fields[columnnum(self.header, "repEnd")])-int(fields[columnnum(self.header, "repStart")])
        else:
            repstart = int(fields[columnnum(self.header, "repStart")])
            repsize = int(fields[columnnum(self.header, "repEnd")])-int(fields[columnnum(self.header, "repLeft")])
        chrsize = int(fields[columnnum(self.header, "genoEnd")])-int(fields[columnnum(self.header, "genoLeft")])
        # Variables for external use:
        self.repName = fields[columnnum(self.header, "repName")].strip()
        self.repSize = repsize
        self.chrName = fields[columnnum(self.header, "genoName")].strip()
        self.chrSize = chrsize
        self.score = int(fields[columnnum(self.header, "swScore")])
        self.strand = fields[columnnum(self.header, "strand")].strip()
        self.alignStart = int(fields[columnnum(self.header, "genoStart")])
        self.alignEnd = int(fields[columnnum(self.header, "genoEnd")])
        self.matchStart = repstart
        self.matchEnd = int(fields[columnnum(self.header, "repEnd")])
        self.repID = self.NullString
    def parseDfam(self):
        fields = self.line.split('\t')
        # Conversions
        if fields[columnnum(self.header, "strand",8)] == "-":
            start = fields[columnnum(self.header, "alignment end",10)]
            end = fields[columnnum(self.header, "alignment start",9)]
        else:
            start = fields[columnnum(self.header, "alignment start",9)]
            end = fields[columnnum(self.header, "alignment end",10)]
        # Variables for external use:
        self.repName = fields[columnnum(self.header, "model name",2)].strip()
        self.repSize = int(fields[columnnum(self.header, "hmm length",7)])
        self.chrName = fields[columnnum(self.header, "#sequence name",0)].strip()
        self.chrSize = int(fields[columnnum(self.header, "sequence length",13)])
        self.score = int(float(fields[columnnum(self.header, "bit score",3)]))
        self.strand = fields[columnnum(self.header, "strand",8)].strip()
        self.alignStart = int(start)
        self.alignEnd = int(end)
        self.matchStart = int(fields[columnnum(self.header, "hmm start",6)])
        self.matchEnd = int(fields[columnnum(self.header, "hmm end",7)])
        self.repID = self.NullString
    def parseGtf(self):
        fields = self.line.split('\t')
        # Get the name from the other attributes column
        # If following the offical specification the first 'other' attribute should be gene_id
        # NOTE: Gene_id should be a unique id. Using this for the repeat name may cause issues! Therefore its use should be documented.
        # TODO: Check all attributes looking for a repName key before resorting to the first value as a last resort.
        otherAttributes = fields[8]
        firstAttribute = otherAttributes.split(';')[0]
        firstAttribute = firstAttribute.replace('='," ")  # Change = to space if = is used
        repID = firstAttribute.split(' ')[-1].strip()
        repID = repID.replace('"',"")                   # Remove quotes if used
        repID = repID.replace("'","")                   # Remove quotes if used
        # Variables for external use:
        # Uncomment/comment relevant lines depending on which column to use for the repeat name.
        self.repName = fields[2].strip()                  # Feature column as repeat name
        self.repSize = self.NullInt
        self.chrName = fields[0].strip()
        self.chrSize = self.NullInt
        if fields[5]==".":                                # Missing values are replaced with a period
            self.score = self.NullInt
        else:
            self.score = int(fields[5])
        self.strand = fields[6].strip()
        self.alignStart = int(fields[3])
        self.alignEnd = int(fields[4])
        self.matchStart = self.NullInt
        self.matchEnd = self.NullInt
        self.repID = repID                              # Gene name used as a repeat ID
    # Conversion functions specific to certain file types implemented here
    # incase other file type are added later which share these functions
    def getAlignStart53(self):
        if self.strand == "-":
            start = self.alignEnd
        else:
            start = self.alignStart
        return start
    def getAlignEnd53(self):
        if self.strand == "-":
            end = self.alignStart
        else:
            end = self.alignEnd
        return end
    def getChrLeft(self):
        if self.chrSize != self.NullInt:            # Only calculate if chrSize has been parsed
            chrLeft = 0-(self.chrSize-self.alignEnd)
        else:
            chrLeft = self.NullInt
        return chrLeft
    def getMatchLeft53(self):
        if self.type != "BED" and self.type != "GTF":   # BED and GTF formats don't store the required values
            if self.strand == "-":
                matchLeft = self.matchStart
            else:
                matchLeft = 0-(self.repSize-self.matchEnd)
        else:
            matchLeft = self.NullInt
        return matchLeft
    def getMatchStart53(self):
        if self.type != "BED" and self.type != "GTF":
            if self.strand == "-":
                matchStart = 0-(self.repSize-self.matchEnd)
            else:
                matchStart = self.matchStart
        else:
            matchStart = self.NullInt
        return matchStart

# Function to detect file type
# Note: The DFAM and UCSC file endings are not standard, but added as an alternative way to manually identify a file.
def detectFileType(fileobj):
    type = None
    # Check for UCSC or DFAM headers
    header = fileobj.readline()
    start = header.split()[0].strip()
    # Check filetype extensions
    if fileobj.name[-3:].upper()=="BED":
        type = "BED"
    elif fileobj.name[-3:].upper()=="GTF" or fileobj.name[-3].upper()=="GFF":
        type = "GTF"
    elif fileobj.name[-3:].upper()=="FAM": # or fileobj.name[-4:].upper()=="HITS": # Uncomment to allow DFAM .hits extension (not used currently as may not be unique to DFAM)
        type = "DFAM"
    elif fileobj.name[-3:].upper()=="CSC":
        type = "UCSC"
    # If filetype extensions unclear check first line.
    elif start.upper() in ["BIN","#BIN"]:
        type = "UCSC"
    elif start.upper() in ["SEQUENCE","#SEQUENCE"]:
        type = "DFAM"
    fileobj.seek(0)     # Return file pointer to the start
    return type

# Class to index an annotation file and to facilitate loading of its contents as annotation objects
class loadTrackFile(object):
    """Indexs an annotation file and allows for entries to be retrieved by line number or region"""
    def __init__(self, fileobj, filetype="", fixedannotype="", indexlines=0, smallonly=0):
        # Initalise object variables
        self.warningmsg = ""
        self.annoType = fixedannotype   # Some annotation files may not list a type as they are exclusivly one type
        self.ordered = 1                # Chromosomes are grouped together
        self.sorted = 1                 # The file is sorted by start position
        self.fileobj = fileobj
        self.cachedEntries = []
        self.smallonly = smallonly      # Variable stored with the object for use by external functions interacting with the object
        if filetype=="":
            self.type=detectFileType(self.fileobj)
        else:
            self.type=filetype.upper()
        # Store the first line incase it is a header line needed later
        self.fileobj.seek(0)
        line = self.fileobj.readline()
        self.header = line              # Store the first line as a header regardless
        while line[0]=="#":
            self.header = line          # Replace with the last comment line if multiple lines are present
            line = self.fileobj.readline()
        self.fileobj.seek(0)
        # Index the file for faster access times later
        self.indexFile()
        if indexlines:
            self.indexLines()
    def indexFile(self):
        """Create an index of chromosome start positions to speed up file access and check annotation order"""
        # NOTE: Using the annotation object to parse each line slows startup considerably. (approx factor of 4)
        #starttime2 = time.time() # Index benchmarking line
        self.fileobj.seek(0)
        curChr = ""
        curStart = -1
        position = 0
        indexChr = {}
        line = self.fileobj.readline()
        while line:
            if line[0] != "#":                          # Ignore commonly used comment characters
                if self.type=="GTF":                    # Process fixed positions without Annotation class overhead
                    fields = line.split('\t')
                    chrName = fields[0].strip()
                    startpos = int(fields[3])
                elif self.type=="BED":
                    fields = line.split('\t')
                    chrName = fields[0].strip()
                    startpos = int(fields[1])
                else:
                    annoentry = Annotation(line,self.type,self.header)
                    chrName = annoentry.chrName
                    startpos = annoentry.alignStart
                chrName = chrName.upper()
                # Check if the annotations are ordered by start position, smallest to largest
                if startpos<curStart and chrName==curChr:   # Check if the start position has decreased while the chromosome has stayed the same
                    self.sorted = 0
                curStart = startpos
                # Check chromosomes are grouped together and store the start position for each chromsome
                if chrName!=curChr:         # If the new chr name is different, update the start position
                    if chrName not in indexChr:
                        position = self.fileobj.tell()-len(line)
                        indexChr[chrName] = position
                    else:                               # NOTE: Need to account for unordered files!
                        #print("WARNING: File not sorted by chromosome, access times will be longer.")
                        self.warningmsg = "WARNING: File not grouped by chromosome, access times will be longer."
                        self.ordered = 0
                        self.sorted = 0
                    curChr = chrName
            line=self.fileobj.readline()
        self.chrIndex = indexChr
        #print("Time to index: "+str(time.time()-starttime2)) # Index benchmarking line
    def indexLines(self):
        """Create an index of start positions for each line, as a list"""
        # Reduces memory usage compared to using readlines - but does make sorting by column harder
        self.fileobj.seek(0)
        pos=[]
        line=self.fileobj.readline()
        while line:
            if line[0] != "#":                          # Ignore commonly used comment characters
                pos.append(self.fileobj.tell()-len(line))
            line=self.fileobj.readline()
        self.lineIndex = pos
    def loadItems(self, chr, start, end):
        """Load annotations in a specified region into a list"""
        displayItems = []
        chr = chr.upper()
        if chr not in self.chrIndex:
            self.warningmsg = "WARNING: chromosome not found in this file."
        else:
            self.fileobj.seek(self.chrIndex.get(chr))   # Go to the start of the chromosome
            line = self.fileobj.readline()
            while line:
                annoentry = Annotation(line,self.type,self.header)
                # Long if statement to check if the annotation spans the range completely, starts in the range or ends in the range.
                # NOTE: Removal of the first <= and >= in the below line will omit annotations of the exact same length.
                if annoentry.chrName.upper()==chr and ((annoentry.alignStart<=start and annoentry.alignEnd>=end) or (annoentry.alignStart>=start and annoentry.alignStart<=end) or (annoentry.alignEnd>=start and annoentry.alignEnd<=end)):
                    # Store annotation
                    displayItems.append(annoentry)
                    # Load the next line
                    line=self.fileobj.readline()
                elif self.ordered==1 and annoentry.chrName.upper()!=chr:
                    line=None                       # File is in chr order so stop searching for entries
                elif self.sorted==1 and annoentry.alignStart>end:
                    line=None                       # File is sorted by start position so stop searching for additional entries
                else:
                    line=self.fileobj.readline()    # File is not in order so continue to the end. TODO: Handle this better in indexing.
        self.cachedEntries = displayItems
    def loadLine(self, line):
        """Loan a specific annotation into memory using the line number"""
        if type(line) is int:   # If a number is passed load the line from the file, else treat as line content
            # Treat numbers below 0 as 0 and numbers above the highest line number as the last line
            if line<0:
                line=0
            elif line+1>len(self.lineIndex):
                line=len(self.lineIndex)-1
            self.fileobj.seek(self.lineIndex[line])
            line=self.fileobj.readline()
        annoentry = Annotation(line,self.type,self.header)
        return annoentry
