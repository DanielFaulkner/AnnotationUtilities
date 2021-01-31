# libAnnoFeat
# Functions to add columns which add details to annotations on nearby ]features
#
# By Daniel R Faulkner

# TODO: This method of lookup, using the code in the trackobj, is very slow.
#       Checking each annotation against each annotation in the same chromosome.
#       This could be improved dramatically using alternative techniques.
# TODO: Write a separate function for copying preceeding comment lines and returning the last comment line, for modification/access

from lib import libAnnoShared

EmptyName = "Genomic"   # The name to use for regions with no features
EmptyPriority = 0       # The priority value to give regions with no features (setting to a negative number will cause any item to take priority)
featuredict = {             # Dictionary of features to display, along with their character and priority
    'exon':["#",10],        # Duplicated from libAnnoView incase a different config is required
    'transcript':["-",5]
}

# featureOverlap: Takes a region and looks up within a track object what features are present
# Optional TODO: Could add a 'mixed' feature type based on feature list length
# Simple usage example:
#trackobj = libAnnoShared.loadTrackFile(open("RefFilename"))   # Load the files into a track object
#type, name = featureOverlap('chr1',0,1000, trackobj)          # Returns the type and name of any feature(s) at that region
def featureOverlap(chr, start, end, reftrackobj, returnall=0):
    """Compares two annotation files and reports any overlapping features"""
    # Load the features from the track object
    reftrackobj.loadItems(chr, start, end)      # NOTE: Function is not optimised for multiple calls
    featurelist = reftrackobj.cachedEntries
    featureOut = ""
    featureOutID = ""
    # Return all results
    if returnall:   # If returning all features (need to remove duplicate types)
        types = []
        names = []
        for item in featurelist:            # Produce unique lists of feature types and names
            if item.repName not in types:
                types.append(item.repName)
            if item.repID not in names:
                names.append(item.repID)
        for item in types:                  # Turn the lists into strings
            featureOut = featureOut+item+"; "
        for item in names:
            featureOutID = featureOutID+item+"; "
        featureOut=featureOut[:-2]          # Remove the trailing semi colon
        featureOutID=featureOutID[:-2]
    # Return results with highest priority
    else:           # Else return the feature with the highest priority
        names = []
        featureOut = EmptyName
        featurePriority = EmptyPriority
        newPriority = EmptyPriority
        for item in featurelist:
            if item.repName in featuredict:         # Update priority
                newPriority = featuredict.get(item.repName)[1]
            else:
                newPriority = 0
            if newPriority>featurePriority:         # Restart if the priority is higher
                featurePriority=newPriority
                featureOut=item.repName
                names = [item.repID]
            elif newPriority==featurePriority:      # Add to existing if priority is equal
                if item.repID not in names:
                    names.append(item.repID)
        for item in names:                          # Turn the list of names into a string
            featureOutID = featureOutID+item+"; "
        featureOutID=featureOutID[:-2]              # Remove the trailing semi colon
    # Default value if no features overlap
    if featureOut == "":
        featureOut = EmptyName
    return featureOut, featureOutID

# featureAddColumn: Adds to an annotation file 2 additional columns for the type and name of other features present.
# Options:
# - margin increases the size of the area to include (in bps)
# - title sets the preceeding part of the column headings
# - returnall (0/1) returns all features instead of those with the highest priority
# Simple usage example:
#trackobj = libAnnoShared.loadTrackFile(open("RefFilename.gtf"))            # Load the files into a track object
#featureAddColumn(open('queryfile.bed'), trackobj, open('output.tsv','w'))  # Outputs a file with additional columns on nearby features
def featureAddColumn(annofileobj, reftrackobj, outfileobj, margin=0, title="", returnall=0):
    """Adds a column detailing the feature in a region"""
    type = libAnnoShared.detectFileType(annofileobj)
    annofileobj.seek(0)
    # Check for header line and add title column header (assuming last comment before datalines)
    line = annofileobj.readline()
    header = ""
    while line[0]=="#":
        if title!="":
            header = line.strip() + "\t" + title+" types\t"+title+" names\n"
        else:
            header = line.strip() + "\tFeature Types\tFeature Names\n"
        line = annofileobj.readline()
    outfileobj.write(header)    # NOTE: If multiple preceeding comment lines present they will not be preserved using this method
    # For each data line open the annotation position and perform comparison
    while line:
        if line[0]!="#":    # Ignore comment lines
            annoObj = libAnnoShared.Annotation(line,type,header)    # Parse the annotation
            featurename, featureID = featureOverlap(annoObj.chrName,annoObj.alignStart-margin,annoObj.alignEnd+margin,reftrackobj,returnall)
            newline = line.strip()+"\t"+featurename+"\t"+featureID+"\n"
            outfileobj.write(newline)
        line = annofileobj.readline()
        # Uncomment to have comment lines preserved:
        #else:
        #   outfileobj.write(line)
