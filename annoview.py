#!/usr/bin/python3
# annoview.py
#
# A console program to view two annotation files (or any files saved in a supported format) side by side
#
# By Daniel R Faulkner

# Locations for downloading gtf files for genome wide comparisons:
# https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/genes/
# https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/reference/GCF_000001405.39_GRCh38.p13/

# Lines needed for benchmarking loading times
#import time
#start = time.time()

import shutil   # Needed to get the terminal size
from lib.libAnnoView import *

# Object which accepts user input and displays the requested information
class controlPane(object):
    """Parses user input and formats the display accordingly"""
    def __init__(self, queryfileobj, reffileobj, activeline=1, viewsize=10000, featureview = 5):
        """Create the summary of closest items object"""
        self.activeline = activeline
        self.queryfileobj = queryfileobj
        self.reffileobj = reffileobj
        self.viewsize = viewsize
        self.featurewinsize = featureview
        self.raw=0
        self.preprocess()
        self.loadDisplay()
        #print("Loading took: "+str(time.time()-start))  # Use to benchmark loading times
        self.input()
    def input(self):
        """Parse user input, also acts as the programs mainloop"""
        exit = 0
        while not exit:
            command = input(': ')
            # Parse input
            try:
                self.activeline = int(command)
            except:
                pass
            if command.lower() == "exit":
                exit=1
            elif command.lower() == "help":
                self.showHelp()
            elif command.lower() == "zoomin":
                self.viewsize=int(self.viewsize/2)
            elif command.lower() == "zoomout":
                self.viewsize=int(self.viewsize*2)
            elif command.lower() == "viewall":
                self.queryobj.smallonly=1
                self.refobj.smallonly=1
            elif command.lower() == "viewlarge":
                self.queryobj.smallonly=0
                self.refobj.smallonly=0
            elif command.lower() == "viewall query":
                self.queryobj.smallonly=1
            elif command.lower() == "viewlarge query":
                self.queryobj.smallonly=0
            elif command.lower() == "viewall ref":
                self.refobj.smallonly=1
            elif command.lower() == "viewlarge ref":
                self.refobj.smallonly=0
            elif command.lower() == "query r":
                self.fileWin.shiftViewRight()
            elif command.lower() == "query l":
                self.fileWin.shiftViewLeft()
            elif command.lower() == "query unedited":
                self.raw=1
            elif command.lower() == "query edited":
                self.raw=0
            # Refresh the display, provided the program isn't in the process of exiting
            if exit==0:
                self.loadDisplay()
        print("Good bye")
    def preprocess(self):
        """Load the tracks and objects"""
        print("Loading and preprocessing "+self.queryfileobj.name)
        self.queryobj = loadTrackFile(self.queryfileobj, indexlines=1)
        print("Loading and preprocessing "+self.reffileobj.name)
        self.refobj = loadTrackFile(self.reffileobj)
        # Create the window class objects
        print("Processing items to display")
        curentry = self.queryobj.loadLine(self.activeline)
        self.refobj.loadItems(curentry.chrName,curentry.alignStart-self.viewsize,curentry.alignEnd+self.viewsize)
        self.queryobj.loadItems(curentry.chrName,curentry.alignStart-self.viewsize,curentry.alignEnd+self.viewsize)
        self.tracks = [self.queryobj,self.refobj]
        # Initial object creation, and display
        self.setPaneSizes(self.featurewinsize)
        self.fileWin = fileviewPane(self.queryobj,self.filewinSize,self.raw,self.activeline)
        self.genomeWin = viewGenome(self.tracks,curentry.chrName,curentry.alignStart-self.viewsize,curentry.alignEnd+self.viewsize)
        self.viewWin = viewClosest(curentry.chrName,curentry.alignStart-self.viewsize,curentry.alignEnd+self.viewsize, self.refobj,self.viewwinSize,1)
    def loadDisplay(self):
        """Refresh the display used first cached then new data"""
        # Update the positions in the classes:
        curentry = self.queryobj.loadLine(self.activeline)
        self.genomeWin.setPosition(curentry.chrName,curentry.alignStart-self.viewsize,curentry.alignEnd+self.viewsize)
        self.viewWin.setPosition(curentry.alignStart-self.viewsize,curentry.alignEnd+self.viewsize)
        # Update the display with any stored data in memory (ie if zooming out/in)
        self.setPaneSizes(self.featurewinsize)
        self.fileWin.displayRefresh(self.filewinSize,self.raw,self.activeline)
        self.genomeWin.displayPane()
        self.viewWin.displayPane(self.viewwinSize)
        # Update the cache
        print("*Updating file cache*", end=" ")
        self.refobj.loadItems(curentry.chrName,curentry.alignStart-self.viewsize,curentry.alignEnd+self.viewsize)
        self.queryobj.loadItems(curentry.chrName,curentry.alignStart-self.viewsize,curentry.alignEnd+self.viewsize)
        print()
        # Refresh the display
        self.fileWin.displayRefresh(numlines=self.filewinSize,raw=self.raw, active=self.activeline)
        self.genomeWin.displayPane()
        self.viewWin.displayPane(self.viewwinSize)
    def setPaneSizes(self, lines=5):
        """Set the size of the display windows"""
        self.termsize = shutil.get_terminal_size((80,20))
        usedlines=3+(len(self.tracks)*3)        # Header for each pane and the bottom control line + number of tracksx3
        minquerysize = 3
        # Check view size is sensible:
        if lines<1:
            lines=1
        elif lines>(self.termsize[1]-(usedlines+minquerysize)):
            lines=self.termsize[1]-(usedlines+minquerysize)
        # Calculate the height of each display
        if usedlines+lines+3>self.termsize[1]:  # Set a minimum size for the view closest window
            self.viewwinSize=self.termsize[1]-(usedlines+lines+3)
        else:
            self.viewwinSize = lines
        # Remainder is used for the file window
        self.filewinSize = self.termsize[1]-(usedlines+self.viewwinSize)
    def showHelp(self):
        """Display a help window with the available commands"""
        print()
        print("This genome comparison tools accepts the following inputs:")
        print("<number>\tLine to load from file window (top)")
        print("zoomin\tIncreases magnification of the genome window")
        print("zoomout\tDecreases magnification of the genome window")
        print("viewall\tShows all items in the genome window (use viewall ref/query to specify a track)")
        print("viewlarge\tHides items which are smaller than a character")
        print("query r\tMoves the query view to the right (if lines extend beyond the screen)")
        print("query l\tMoves the query view to the left (if lines extend beyond the screen)")
        print("query unedited\tShows the query annotations unedited")
        print("query edited\tShows the query annotations in a standardised format")
        print("'exit'\tCloses the program")
        print()
        input('Press enter to continue')

# Parse command line input

def consoleUI():
    """Process command line arguments and pass them onto the controlPane object"""
    import argparse
    parser = argparse.ArgumentParser(description="Annotation viewer for visual side by side comparisons")
    # Required arguments
    parser.add_argument("queryfile", help="Path to query file", type=argparse.FileType('r'))
    parser.add_argument("referencefile", help="Path to reference file", type=argparse.FileType('r'))
    # Optional Arguments
    parser.add_argument("-l","--line", help="Goto line", nargs=1, type=int)
    parser.add_argument("-z","--zoom", help="Zoom level (bp)", nargs=1, type=int)
    parser.add_argument("-f","--features", help="Nearby feature display size", nargs=1, type=int)
    # Parse
    args = parser.parse_args()

    # Setup variables
    line = 0
    if args.line:
        line = args.line[0]
    zoom = 10000
    if args.zoom:
        zoom = int((args.zoom[0])/2) # Divide the value by two as view size is the size either side
    features = 5
    if args.features:
        features = args.features[0]+1

    # Start program
    controlPane(args.queryfile, args.referencefile, line, zoom, features)

if __name__ == "__main__":
    consoleUI()
