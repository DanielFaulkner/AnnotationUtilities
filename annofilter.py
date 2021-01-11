#!/usr/bin/python3
# annofilter
#
# A terminal prompt interface to filter entries within a L1 annotation file.
#
# By Daniel R Faulkner

from lib import libAnnoShared
from lib import libAnnoFilter
import argparse
import sys

# Process function:
def processInput(fileinobj, fileoutobj, type):
    """Process the arguments, running the relevant filters"""
    # Open the input file and get the header if applicable
    if type == "BED" or type == "GTF":  # GTF can have a header in the form of a comment line, but column positions are fixed
        header = ""
    else:
        # Headers lines are required for DFAM and UCSC file types for the software to correctly parse the file.
        header = fileinobj.readline()   # TODO: Add error checking to ensure these are header lines (Easiest maybe to check if any value can be converted to an int)
        fileoutobj.write(header)
    # Process annotations
    error=0
    errorpromoter=0
    for line in fileinobj:
        remove = 0
        if line[0] != "#":      # Ignore comment lines (Write out)
        # Process entry
            entry = libAnnoShared.Annotation(line, type, header)
            if args.score and remove == 0:
                passed = libAnnoFilter.filterMinScore(entry, args.score[0])
                if passed<1:
                    if passed<0:
                        error=1
                    remove = 1
            if args.size and remove == 0:
                passed = libAnnoFilter.filterMinSize(entry, args.size[0])
                if passed<1:
                    if passed<0:
                        error=1
                    remove = 1
            if args.reqregion and remove == 0:
                passed = libAnnoFilter.filterReqRegion(entry, args.reqregion[0], args.reqregion[1])
                if passed<1:
                    if passed<0:
                        error=1
                    remove = 1
            if args.minpromoter and remove == 0:
                passed = libAnnoFilter.filterMinPromoterBases(entry, promoterenddict, args.minpromoter[0], defaultpromend)
                if passed<1:
                    if passed<0:
                        error=1
                        errorpromoter=1
                    remove = 1
            if args.annonames and remove == 0:
                passed = libAnnoFilter.filterName(entry, annonames, exclude, regex)
                if passed<1:
                    if passed<0:
                        error=1
                    remove = 1
            if args.chrnames and remove == 0:
                passed = libAnnoFilter.filterChromosome(entry, chrnames, exclude, regex)
                if passed<1:
                    if passed<0:
                        error=1
                    remove = 1
        if remove==0:
            fileoutobj.write(line)
    if error==1:
        print("Warning: One or more of annotations caused errors.")
        print("This maybe because the required annotation fields were not present in the source annotation file.")
        print("These entries have not been included in the output file.")
    if errorpromoter==1:
        print("- Error was within the promoter filter. It is possible some entries are of zero length.")
    # Close files
    fileinobj.close()
    fileoutobj.close()

## Command line options:
### Parse the command line arguments
parser = argparse.ArgumentParser(description="Annotation filter")
# Arguments:
# Required
parser.add_argument("-i","--input", help="Input filename", type=argparse.FileType('r'))
parser.add_argument("-o","--output", help="Output filename", type=argparse.FileType('w'))
# Optional
parser.add_argument("-t","--type", help="Input filetype", action="store")
parser.add_argument("--score", help="Minimum score", nargs=1, type=int)
parser.add_argument("--size", help="Minimum size", nargs=1, type=int)
parser.add_argument("--reqregion", help="Required region", nargs=2, type=int)
parser.add_argument("--minpromoter", help="Minimum bases in promoter", nargs=1, type=int)
parser.add_argument("--orfs", help="Open Reading Frame filename", type=argparse.FileType('r'))
parser.add_argument("--defaultend", help="Default promoter end", nargs=1, type=int)
parser.add_argument("--annonames", help="Annotation names", action="store")
parser.add_argument("--chrnames", help="Chromosome names", action="store")
parser.add_argument("--exclude", help="Exclude", action="store_true")
parser.add_argument("--regex", help="Use regular expression string matching", action="store_true")

# Any commands entered without a flag
args = parser.parse_args()

### Checking user input
error = 0
if not args.input:
    print("Input filename required")
    error = 1
if not args.output:
    print("Output filename required")
    error = 1

if error==1:
    print("\nAnnotation file filter requires an input file and output filename.\n")
    sys.exit()

if args.minpromoter and not (args.orfs or args.defaultend):
    print("\nFiltering by the number of bases in the promoter requires knowledge of promoter size.\n")
    print("\nPlease use either or both the defaultend or orfs options.\n")
    sys.exit()

if not args.type:
    type = libAnnoShared.detectFileType(args.input)
    if not type:
        print("\nInput file type could not be detected, please specify using the type argument.\n")
        sys.exit()
else:
    type = args.type.upper()
    if type not in ["BED", "DFAM", "UCSC", "GTF"]:
        print("\nAccepted file type options are BED, GTF, DFAM or UCSC.\n")
        sys.exit()

# Pre processing of user inputs

exclude = 0
if args.exclude:
    exclude = 1

regex = 0
if args.regex:
    regex = 1

promoterenddict = {}
if args.orfs:
    orffileobj=args.orfs
    promoterenddict = libAnnoFilter.genPromEndDict(orffileobj)
    orffileobj.close()

defaultpromend = 0
if args.defaultend:
    defaultpromend = args.defaultend[0]

annonames = []
if args.annonames:
    annonames = args.annonames.split(',')

chrnames = []
if args.chrnames:
    chrnames = args.chrnames.split(',')

### Processing the conversion

processInput(args.input,args.output,type)
