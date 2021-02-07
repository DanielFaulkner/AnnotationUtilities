# libAnnoView
# Functions relating to the processing of annoation files and displaying the contents.
#
# By Daniel R Faulkner

import shutil   # Needed to get the terminal size
from operator import itemgetter
from lib import libAnnoShared   # Shared functions

# Track characters and their display priority
otherChar = ["~",1]         # Character representation and priority of unknown features
emptyChar = [" ",0]         # Character representation and priority of empty regions
featureignorelist = []      # Names of features to ignore
featuredict = {             # Dictionary of features to display, along with their character and priority
    'exon':["#",10],
    'transcript':["-",5]
}

# viewGenome: Displays simple text representation of the genomic region
# Simple usage example:
#track1 = loadTrackFile(open("filename"))   # Load the files into a track object
#track2 = loadTrackFile(open("filename"))
#track1.loadItems('chr1',0,1000)            # Load into memory the annotations in the region
#track2.loadItems('chr1',0,1000)
#viewGenome([track1,track2],'chr1',0,1000)  # Display a text representation of a region
class viewGenome(object):
    """Displays a text representation of a genomic region"""
    def __init__(self, trackobjs=[], chr="", start=0, end=1000):
        """Setup initial object variables"""
        self.trackobjs = trackobjs    # Track file objects as a list
        # Setting default start positions
        self.chr = chr
        self.start = start
        self.end = end
        self.displayPane()
    def setPosition(self, chr, start, end):
        self.chr = chr
        self.start = start
        self.end = end
    def displayPane(self):
        """Create the basic elements to display on the screen"""
        # Create the templates for the borders
        self.termwidth = shutil.get_terminal_size((80,20))[0]
        border = "="*self.termwidth
        # For each file object print the name and the tracks.
        for trackobj in self.trackobjs:
            if len(trackobj.fileobj.name)>self.termwidth:
                trackname = trackobj.fileobj.name[:-(self.termwidth+1)]+">"
            else:
                trackname = trackobj.fileobj.name
            topLine = trackname+border[len(trackname):]
            self.smallonly = trackobj.smallonly
            trackpos = self.calcTrack(trackobj.cachedEntries,"+")
            trackneg = self.calcTrack(trackobj.cachedEntries,"-")
            print(topLine)
            print(trackpos)
            print(trackneg)
        # Display the bottom border
        start = self.chr+":"+str(self.start)
        end = self.chr+":"+str(self.end)
        botLine = start+border[len(start):-len(end)]+end
        print(botLine)
    def calcTrack(self, objects, strand):
        """Construct the track visualisation"""
        # Calculate which char to display for each position
        trackstr=""
        charWidth = (self.end-self.start)/self.termwidth
        genomePos = self.start+(charWidth/2)
        for charPos in range(self.termwidth):
            newChar=emptyChar
            for dispObj in objects:
                if dispObj.strand==strand:                                      # Check strand
                    if self.smallonly == 1:                                     # Check display type setting
                        charstart = genomePos-(charWidth/2)
                        charend = genomePos+(charWidth/2)
                        if (dispObj.alignStart<charstart and dispObj.alignEnd<charstart) or (dispObj.alignStart>charend and dispObj.alignEnd>charend):
                            pass                                                # Object both start and ends before or after char (replace with not in if statement)
                        else:                                                   # Item present somewhere within the character
                            newChar = self.validObj(dispObj,newChar)
                    elif self.smallonly == 0 and (dispObj.alignStart<genomePos and dispObj.alignEnd>genomePos):
                        if (dispObj.alignEnd-dispObj.alignStart)>charWidth:               # Ignore items smaller than one character
                            newChar = self.validObj(dispObj,newChar)
            trackstr=trackstr+newChar[0]
            genomePos = genomePos+charWidth # Update position for next loop
        return trackstr
    def validObj(self, object, currentType=emptyChar):
        """Given an annotation object determines if the character representation needs updating"""
        if object.repName in featureignorelist:
            newType = currentType
        elif object.repName in featuredict:
            representation = featuredict.get(object.repName)
            if representation[1] > currentType[1]:
                newType = representation
            else:
                newType = currentType
        else:
            if otherChar[1] > currentType[1]:
                newType = otherChar
            else:
                newType = currentType
        return newType

# viewClosest: Displays the closest features, given a location.
# Simple usage example:
#track = loadTrackFile(open("filename"))
#track.loadItems('chr1',0,1000)
#viewClosest('chr1',0,1000,track)
# NOTE: Class regenerates lists with each refresh. Maybe investigate increased use of cached content where applicable.
class viewClosest(object):
    """Displays the closest items, using annotations preloaded into a track file object"""
    def __init__(self, chr="", start=0, end=1000, trackobj=None, lines=3, viewall=1):
        """Creates an object and displays the closest items to the midpoint of a given location"""
        self.preList = []
        self.postList = []
        self.trackobj = trackobj
        self.viewstart = start
        self.viewend = end
        self.viewall = viewall
        self.displayPane(lines)
    def setPosition(self, start, end):
        """Updates the region being viewed"""
        # Chromosome not needed as the entries currently loaded by the track object should be limited to the correct region
        self.viewstart = start
        self.viewend = end
    def createLists(self):
        """Populates the lists of nearest objects and sorts them from closest to most distant"""
        targetpos = int(self.viewstart+((self.viewend-self.viewstart)/2))
        try:    # Incase the function is started without a track file object.
            self.objects = self.trackobj.cachedEntries
        except:
            self.objects = []
        # Emptry lists of existing data
        self.preList = []
        self.postList = []
        # Order by location in two lists, one pre one post
        for item in self.objects:
            size = item.alignEnd-item.alignStart
            if size<((self.viewend-self.viewstart)/self.termwidth):
                visible="N"
            else:
                visible="Y"
            if not self.viewall and visible=="N":
                pass    # Not the best use of the if command, but easier to read this way round
            else:
                if item.alignStart>targetpos:
                    self.postList.append((item.alignStart,item.alignEnd,item.repName,item.repID, visible))
                else:
                    # Pre list may also overlapping items
                    self.preList.append((item.alignStart,item.alignEnd,item.repName,item.repID, visible))
        self.postList.sort(key=itemgetter(0))               # Sort by start (smallest to largest)
        self.preList.sort(key=itemgetter(1),reverse=True)   # Sort by end   (largest to smallest)
    def displayPane(self, lines=3):
        """Display this number of rows to the screen"""
        self.termwidth = shutil.get_terminal_size((80,20))[0]
        self.createLists()
        colWidth = int(self.termwidth/2)
        # Title
        space = " "*self.termwidth
        titlept1 = "Immediately preceding"
        titlept2 = "Immediately following"
        title = titlept1+space[len(titlept1):-colWidth]+titlept2
        print(title)
        # Rows:
        count = lines-1
        coltemp = "{}:{}-{} {} {}"
        while count:
            # Columns: visible, Start, End, Type, Name
            try:
                preentry = self.preList.pop(0)
                prestr=coltemp.format(preentry[4],preentry[0],preentry[1],preentry[2],preentry[3])
            except:
                prestr = ""
            try:
                postentry = self.postList.pop(0)
                poststr=coltemp.format(postentry[4],postentry[0],postentry[1],postentry[2],postentry[3])
            except:
                poststr = ""
            # - Trim to required size and print
            lineout = prestr[:colWidth]+space[len(prestr[:colWidth]):-colWidth]+poststr[:colWidth]
            print(lineout)
            # Advance counter
            count=count-1

# fileviewPane: Displays the query file, with arguments to indicate the number of rows, the type of display format and which line is active
# Note: Currently no benefit to being within a class as there is no refresh function.
# Simple usage example:
#track = loadTrackFile(open("filename"),"","",1)    # Line index is required
#fileviewPane(track)
# TODO: Shifting the view to the right hides the current line indicator (also the line continues indicator obscures the last char of the previous view)
class fileviewPane(object):
    """Displays the query file"""
    def __init__(self, trackobj, lines=5, raw=0, active=0):
        """Create the object from the query file object, the number of lines to display and which one to mark as active"""
        # Store the provided variables
        self.trackobj = trackobj
        self.numlines = lines
        self.active = active
        self.raw = raw
        # Variables for storing additional information
        self.filesize = len(self.trackobj.lineIndex)    # Number of lines
        self.currentlines = []
        self.termwidth = shutil.get_terminal_size((80,20))[0]
        self.currentview = [0,self.termwidth]
        # Create the window
        self.createLines()
        self.displayRefresh()
    def createLines(self):
        """Create formatted lines for each entry and store them in a list"""
        self.currentlines = []
        midpos = int(self.numlines/2)
        posmodifier = 0                         # Modifier to account for the top and bottom of the file
        count = 0
        while count<self.numlines:
            # Extra code for sane scrolling behaviour
            loadpos = self.active+(count-midpos)         # Keeps the selected fields in the middle of the window
            loadpos = loadpos+posmodifier
            if loadpos<0:                           # Correct for the top of the file
                posmodifier=0-loadpos
                loadpos=loadpos+posmodifier
            if (loadpos+self.numlines)>(self.filesize+count):    # Correct for the end of the file
                posmodifier=0-((loadpos+self.numlines)-(self.filesize))
                loadpos=loadpos+posmodifier
            # For both raw and processed outputs get the lines
            if self.raw:
                self.trackobj.fileobj.seek(self.trackobj.lineIndex[loadpos])
                line = self.trackobj.fileobj.readline()
                line = line.replace("\t"," ").strip()   # To condense the raw lines replace tabs with a single space
            else:
                # Change this to reflect the prefered line format
                annotation = self.trackobj.loadLine(loadpos)
                linetemplate = "{}:{}-{}({})  {}:{}  {}({}-{})"
                line = linetemplate.format(annotation.chrName,annotation.alignStart,annotation.alignEnd,annotation.strand,annotation.repName,annotation.repID,annotation.score,annotation.matchStart,annotation.matchEnd)
            if loadpos == self.active:                           # Indicate which line is active
                cursor = "*"
            else:
                cursor = " "
            completeline=cursor+line
            self.currentlines.append(completeline)
            count=count+1
    def displayPane(self):
        """Display lines from the track object cropped to size"""
        fileLineTotal = len(self.trackobj.lineIndex) # Need to know when to stop requesting additional lines (Note len starts at one, list index starts at 0)
        # Pane title
        border = "="*self.termwidth
        titletxt = "File: "+self.trackobj.fileobj.name+" Line: "+str(self.active)+"/"+str(self.filesize-1)+" "
        title = titletxt+border[len(titletxt):]
        print(title)
        # Pane entries
        for completeline in self.currentlines:
            croppedline = completeline[self.currentview[0]:self.currentview[1]]
            if len(completeline)>self.currentview[1]:    # Indicate which lines are longer than the screen
                croppedline=croppedline[:-1]+">"
            print(croppedline)
    def shiftViewRight(self):
        """Shift the part of the line to display to the right"""
        longestentry = 0
        for line in self.currentlines:
            if len(line)>longestentry:
                longestentry = len(line)
        if self.currentview[1]<longestentry:
            self.currentview = [self.currentview[0]+self.termwidth,self.currentview[1]+self.termwidth]
    def shiftViewLeft(self):
        """Shift the part of the line to display to the left"""
        if self.currentview[0]>0:
            self.currentview = [self.currentview[0]-self.termwidth,self.currentview[1]-self.termwidth]
    def displayRefresh(self, numlines=-1, raw=-1, active=-1):
        """Refresh the display, updating the object variables with any new variables passed in"""
        change = 0
        if numlines!=-1 and numlines!=self.numlines:
            self.numlines = numlines
            change = 1
        if raw!=-1 and raw!=self.raw:
            self.raw = raw
            change = 1
        if active!=-1 and active!=self.active:
            self.active = active
            change = 1
        if change:
            self.createLines()
        currentwidth = shutil.get_terminal_size((80,20))[0]
        if self.termwidth != currentwidth:
            self.termwidth = currentwidth
            self.currentview[1]=self.currentview[1]-(self.currentview[1]-self.termwidth)
        self.displayPane()
