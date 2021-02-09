# libAnnoSort
# Functions related to the sorting of annotation files.
#
# By Daniel R Faulkner

from lib import libAnnoShared

# Groups annotations within a file by chromsome and sorts by start position.
# Example usage:
#trackobj = libAnnoShared.loadTrackFile(open("AnnotationFilename"))     # Create track object from file
#sort(trackobj, open('OutputFilename','w'))                             # Perform sort
def sort(trackobj, outputfile):
    """Sort an annotation file by genomic position"""
    trackobj.fileobj.seek(0)
    # Copy any preceeding comment lines across unaltered
    line = trackobj.fileobj.readline()
    while line[0]=="#":
        outputfile.write(line)
        line = trackobj.fileobj.readline()
    # Sort and store the chromosome list
    chrlist = sorted(trackobj.chrIndex)
    for chromsome in chrlist:
        chrlineindex = []
        trackobj.fileobj.seek(trackobj.chrIndex.get(chromsome.upper()))
        # Create a list of alignment start positions and line positions
        line = trackobj.fileobj.readline()
        while line:
            if line[0]!="#":
                annoentry = libAnnoShared.Annotation(line, trackobj.type, trackobj.header)
                if annoentry.chrName.upper()==chromsome:
                    chrlineindex.append([annoentry.alignStart,trackobj.fileobj.tell()-len(line)])
                elif annoentry.chrName.upper()!=chromsome and trackobj.ordered==1:
                    line = None
            if line:
                line = trackobj.fileobj.readline()
        # Sort the start positions
        sortedlinestarts = sorted(chrlineindex)
        # Write out the lines in the correct order
        for item in sortedlinestarts:
            trackobj.fileobj.seek(item[1])
            line = trackobj.fileobj.readline()
            outputfile.write(line)
