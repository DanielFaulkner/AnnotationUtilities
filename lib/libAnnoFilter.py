# libAnnoFilter
# Functions to filter out unwanted entries from an annotation file
#
# By Daniel R Faulkner

from lib.libAnnoShared import columnnum, regexMatch
import re

## Filter functions
# Format: Input element object and variables, perform check, Output yes/no/failure (1/0/-1)

# Minimum quality score
def filterMinScore(annoobj, score=0):
    """Filter by minimum score"""
    passed = 0
    if annoobj.score >= score:
        passed = 1
    return passed

# Minimum total size
def filterMinSize(annoobj, size=0):
    """Filter by minimum size"""
    passed = 0
    annosize=annoobj.alignEnd-annoobj.alignStart
    if annosize >= size:
        passed = 1
    return passed

# Required region
def filterReqRegion(annoobj, start=0, end=0):
    """Filter by required region"""
    passed = 0
    if annoobj.matchEnd==annoobj.matchStart:
        # This element has zero length. Indicating an error or that the information is not available
        passed = -1
    elif annoobj.matchStart<=start and annoobj.matchEnd>=end:
        # Element starts before the required region and ends after.
        passed = 1
    return passed

# Minimum promoter bases
def filterMinPromoterBases(annoobj, promEndDict, bases=0, defaultpromEnd=0):
    """Filter by minimum number of bases within the promoter region"""
    passed = 0
    # Get the end of the promoter region
    if annoobj.repName in promEndDict:
        promoterEnd = promEndDict.get(annoobj.repName)
    else:
        promoterEnd = defaultpromEnd
    # Check the number of bases within the promoter region
    if annoobj.matchStart==annoobj.matchEnd:
        # This element has zero length. Indicating an error or that the information is not available
        passed = -1
    elif annoobj.matchStart<promoterEnd:
        # This element starts before the end of the promoter
        size = min(annoobj.matchEnd,promoterEnd)-annoobj.matchStart
        if size>=bases:
            # The element is longer than the required length
            passed = 1
    return passed

# Annotation name
# Exclude variable toggles between requiring a name or excluding a name
def filterName(annoobj, names=[], exclude=0, regex=0):
    """Filter by annotation name"""
    passed = 0
    if regex==0:
        if exclude == 0 and annoobj.repName in names:
            passed = 1
        elif exclude == 1 and annoobj.repName not in names:
            passed = 1
    else:
        passed = regexMatch(annoobj.repName, names)
    return passed

# Chromosome name
# Exclude variable toggles between requiring a name or excluding a name
def filterChromosome(annoobj, names=[], exclude=0, regex=0):
    """Filter by chromosome name"""
    passed = 0
    if regex==0:
        if annoobj.chrName in names:
            passed = 1
    else:
        passed = regexMatch(annoobj.chrName, names)
    # Swap the values if exclude is set
    if exclude==1:
        if passed:
            passed = 0
        else:
            passed = 1
    return passed

## Supporting Functions

# Produce a dictionary object of first open reading frame positions
# INPUT: The ORF fileobject
# OUTPUT: Dictionary of end positions
def genPromEndDict(fileobj):
	"""Creates a dictionary of promoter end positions for each L1 family."""
	# Parse header:
	header = fileobj.readline()
	NameCol = columnnum(header, "#chrom")		# L1 Name (ie. L1HS)
	StartCol = columnnum(header, "chromStart")	# ORF Start
	EndCol = columnnum(header, "chromEnd")	# ORF End
	orfCol = columnnum(header, "name")		# Gene/ORF name (ie. L1HS_gag)
	# Store values in dictionary
	PromoterEnds = {}
	for line in fileobj.readlines():
		entry = line.split('\t')
		# If L1 name is not in the dictionary add it
		if entry[NameCol] not in PromoterEnds:
			PromoterEnds[entry[NameCol]]=int(entry[StartCol])
		# If the entry in the line is smaller than the current entry then update the entry in the dictionary
		curvalue = int(PromoterEnds.get(entry[NameCol]))
		if curvalue>int(entry[StartCol]):
			PromoterEnds[entry[NameCol]]=int(entry[StartCol])
	return PromoterEnds
