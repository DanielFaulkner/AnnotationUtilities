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

# There are two methods of adding feature details to an annotation file here.
# featureOverlap - Returns the highest priority or all features in a given region.
# featureClosest - Returns the closest feature only in each direction (plus first entry in the file that overlaps)

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
        featureOutID = ""
    return featureOut, featureOutID

# Similar to featureOverlap function but returns closest feature regardless of distance.
# Using the trackobj for the chromosome indexing and checking of file order/sorting it performs.
# *** TODO: Use priority list for 'within' category.
def featureClosest(annotation, reftrackobj, startpos=None, type = ["transcript","exon"], all=1):
    """Returns the closest feature in each direction"""
    featureNameBefore = ""
    featureTypeBefore = ""
    featureDistBefore = -1
    featureStrandBefore=""
    featureNameAfter = ""
    featureTypeAfter = ""
    featureDistAfter = -1
    featureStrandAfter=""
    featureNameWithinList = []
    featureTypeWithinList = []
    featureDistWithin = -1
    featureStrandWithinList = []
    if startpos:
        reftrackobj.fileobj.seek(startpos)
    else:
        reftrackobj.fileobj.seek(reftrackobj.chrIndex.get(annotation.chrName.upper()))   # Go to the start of the chromosome
    line = reftrackobj.fileobj.readline()
    while line:
        if line[0]!="#":
            # Need: Chr/Start/End (then to report ID and type)
            # Possibly manually specify columns for some fixed types to speed up process
            annoentry = libAnnoShared.Annotation(line, reftrackobj.type, reftrackobj.header)
            if annoentry.chrName==annotation.chrName:
                if annoentry.alignEnd<annotation.alignStart:    # Annotation line is before the annotation
                    distance = annotation.alignStart-annoentry.alignEnd
                    if distance<featureDistBefore or featureDistBefore==-1:
                        if type:
                            if annoentry.repName in type:
                                featureDistBefore=distance
                                featureNameBefore=annoentry.repID
                                featureTypeBefore=annoentry.repName
                                featureStrandBefore=annoentry.strand
                        else:
                            featureDistBefore=distance
                            featureNameBefore=annoentry.repID
                            featureTypeBefore=annoentry.repName
                            featureStrandBefore=annoentry.strand
                        if reftrackobj.sorted==1:
                            startpos=reftrackobj.fileobj.tell()-len(line)
                elif annoentry.alignStart>annotation.alignEnd:  # Annotation line is after the annotation
                    distance = annoentry.alignStart-annotation.alignEnd
                    if distance<featureDistAfter or featureDistAfter==-1:
                        if type:
                            if annoentry.repName in type:
                                featureDistAfter=distance
                                featureNameAfter=annoentry.repID
                                featureTypeAfter=annoentry.repName
                                featureStrandAfter=annoentry.strand
                        else:
                            featureDistAfter=distance
                            featureNameAfter=annoentry.repID
                            featureTypeAfter=annoentry.repName
                            featureStrandAfter=annoentry.strand
                        # End at this point if the file is sorted
                        if reftrackobj.sorted == 1 and featureDistAfter!=-1:
                            line=None
                else:                                           # Annotation line is within annotation
                    if type and annoentry.repName not in type:
                        # This annotation type has not been included in the permitted type list
                        pass
                    else:
                        # This annotation is included in the type list or a type list has not been provided
                        featureDistWithin=0
                        if not all and len(featureTypeWithinList)>0:            # Reset the list if a higher priority item is found
                            if annoentry.repName in featuredict:
                                newPriority=featuredict.get(annoentry.repName)[1]
                            else:
                                newPriority=0
                            if featureTypeWithinList[0] in featuredict:
                                oldPriority=featuredict.get(featureTypeWithinList[0])[1]
                            else:
                                oldPriority=0
                            if newPriority>oldPriority:
                                featureTypeWithinList=[]
                                featureNameWithinList=[]
                        if annoentry.repName not in featureTypeWithinList:
                            featureTypeWithinList.append(annoentry.repName)
                        if annoentry.repID not in featureNameWithinList:
                            featureNameWithinList.append(annoentry.repID)
                        if annoentry.strand not in featureStrandWithinList:
                            featureStrandWithinList.append(annoentry.strand)
            else:
                # End if we have moved onto the next chromsome and the file is grouped by chromsome
                if reftrackobj.ordered==1 and annoentry.chrName.upper()!=annotation.chrName.upper():
                    line=None                       # File is in chr order so stop searching for entries
        # Load next line
        if line:
            line=reftrackobj.fileobj.readline()
    # Format the data to be returned
    featureNameWithin = ""
    featureTypeWithin = ""
    featureStrandWithin = ""
    if len(featureNameWithinList)>0:
        if all:
            for item in featureNameWithinList:
                featureNameWithin=featureNameWithin+item+"; "
            for item in featureTypeWithinList:
                featureTypeWithin=featureTypeWithin+item+"; "
            featureNameWithin=featureNameWithin[:-2]
            featureTypeWithin=featureTypeWithin[:-2]
        else:
            featureTypeWithin=featureTypeWithinList[0]
            for item in featureNameWithinList:                  # Displays all results within
                featureNameWithin=featureNameWithin+item+"; "
            featureNameWithin=featureNameWithin[:-2]
            # Replace above 3 lines with: featureNameWithin=featureNameWithinList[0] for just the first result.
    else:
        featureNameWithin=""
        featureTypeWithin=EmptyName
    if featureTypeBefore == "":         # Use the empty type instead of blank space
        featureTypeBefore=EmptyName
    if featureTypeAfter == "":
        featureTypeAfter=EmptyName
    if len(featureStrandWithinList)>1:  # Include the strand information
        featureStrandWithin = "+; -"
    elif len(featureStrandWithinList)==1:
        featureStrandWithin = featureStrandWithinList[0]
    # Return the results
    before = [featureNameBefore,featureTypeBefore,featureDistBefore, featureStrandBefore]
    after = [featureNameAfter,featureTypeAfter,featureDistAfter, featureStrandAfter]
    within = [featureNameWithin,featureTypeWithin,featureDistWithin, featureStrandWithin]
    return before, within, after, startpos

# featureOverlappingAddColumn: Adds to an annotation file 2 additional columns for the type and name of other features present.
# Options:
# - margin increases the size of the area to include (in bps)
# - title sets the preceeding part of the column headings
# - returnall (0/1) returns all features instead of those with the highest priority
# Simple usage example:
#trackobj = libAnnoShared.loadTrackFile(open("RefFilename.gtf"))            # Load the files into a track object
#featureOverlappingAddColumn(open('queryfile.bed'), trackobj, open('output.tsv','w'))  # Outputs a file with additional columns on nearby features
def featureOverlappingAddColumn(annofileobj, reftrackobj, outfileobj, margin=0, title="", returnall=0):
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

# featureClosestAddColumn: Adds to an annotation file 2 additional columns for the type and name of other features present.
# Options:
# - margin increases the size of the area to include (in bps)
# - title sets the preceeding part of the column headings
# - returnall (0/1) returns all features instead of those with the highest priority
# Simple usage example:
#trackobj = libAnnoShared.loadTrackFile(open("RefFilename.gtf"))            # Load the files into a track object
#featureClosestAddColumn(open('queryfile.bed'), trackobj, open('output.tsv','w'))  # Outputs a file with additional columns on nearby features
def featureClosestAddColumn(annofileobj, reftrackobj, outfileobj, senseorder=0, returnall=0):
    """Adds a column detailing the feature in a region"""
    type = libAnnoShared.detectFileType(annofileobj)
    annofileobj.seek(0)
    # Check for header line and add title column header (assuming last comment before datalines)
    line = annofileobj.readline()
    header = ""
    while line[0]=="#":
        header = line
        line = annofileobj.readline()
    extracolstmp = "\t{} Name\t{} Type\t{} Strand\t{} Distance\tWithin Name\tWithin Strand\tWithin Type\tWithin Distance\t{} Name\t{} Type\t{} Strand\t{} Distance\n"
    if senseorder:
        extracols = extracolstmp.format("AntiSense","AntiSense","AntiSense","AntiSense","Sense","Sense","Sense","Sense")
    else:
        extracols = extracolstmp.format("Preceeding","Preceeding","Preceeding","Preceeding","Following","Following","Following","Following")
    newheader = header.strip() + extracols
    outfileobj.write(newheader)    # NOTE: If multiple preceeding comment lines present they will not be preserved using this method
    # For each data line open the annotation position and perform comparison
    startpos=None
    chrPrev = ""
    startPrev = 0
    while line:
        if line[0]!="#":    # Ignore comment lines
            annoObj = libAnnoShared.Annotation(line,type,header)    # Parse the annotation
            if annoObj.chrName!=chrPrev:    # Reset start position for new chromosomes
                startpos=None               # If no start position given the function moves to the start of the chromosome
                chrPrev = annoObj.chrName
            if annoObj.alignStart<startPrev:# Reset start position if the current annotation preceeds the previous one
                startpos=None               # If no start position given the function moves to the start of the chromosome
                startPrev = annoObj.alignStart
            before, within, after, startpos = featureClosest(annoObj, reftrackobj, startpos, [], returnall)
            # Check if we are outputting based on file position or sense/antisense.
            # TODO
            newcolstmp = "\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n"
            if senseorder and annoObj.strand=="-":
                newcols = newcolstmp.format(after[0],after[1],after[3],after[2],within[0],within[1],within[3],within[2],before[0],before[1],before[3],before[2])
            else:
                newcols = newcolstmp.format(before[0],before[1],before[3],before[2],within[0],within[1],within[3],within[2],after[0],after[1],after[3],after[2])
            #newline = line.strip()+"\t"+before[0]+"\t"+before[1]+"\t"+before[2]+"\t"+within[0]+"\t"+within[1]+"\t"+within[2]+"\t"+after[0]+"\t"+after[1]+"\t"+after[2]+"\n"
            newline = line.strip()+newcols
            outfileobj.write(newline)
        line = annofileobj.readline()
        # Uncomment to have comment lines preserved:
        #else:
        #   outfileobj.write(line)
