#!/usr/bin/python3
# annoconv
#
# A terminal prompt interface to convert between different
# L1 annotation file types.
#
# By Daniel R Faulkner

from lib import libAnnoConvert
from lib import libAnnoShared
import argparse
import sys

# Variables (not set from the command line)
NullString = "."    # Value to use when a string conversion is not possible
NullInt = -1         # Number to use when an integer conversion is not possible

# Process function:
def processInput(fileinobj, fileoutobj, type, convert):
    "Process the arguments, performing the requested conversion"
    # Open the input file and get the header if applicable
    if type == "BED" or type == "GTF":
        header = ""
    else:
        header = fileinobj.readline()
    # Open the output file and write the header if applicable
    libAnnoConvert.writeHeader(fileoutobj,convert)
    # Process entries
    for line in fileinobj:
        if line[0] != "#":      # Ignore comment lines
            entry = libAnnoShared.Annotation(line, type, header, NullString, NullInt)
            if convert=="BED":
                fileoutobj.write(libAnnoConvert.BEDline(entry))
            elif convert=="UCSC":
                fileoutobj.write(libAnnoConvert.UCSCline(entry, repclass, repfamily))
            elif convert=="DFAM":
                fileoutobj.write(libAnnoConvert.DFAMline(entry, fixedend))
            elif convert=="GTF":
                fileoutobj.write(libAnnoConvert.GTFline(entry))
    # Close files
    fileinobj.close()
    fileoutobj.close()

## Command line options:
### Parse the command line arguments
parser = argparse.ArgumentParser(description="Annotation file converter")
# Arguments:
parser.add_argument("-i","--input", help="Input filename", type=argparse.FileType('r'))
parser.add_argument("-o","--output", help="Output filename", type=argparse.FileType('w'))
parser.add_argument("-t","--type", help="Input filetype", action="store")
parser.add_argument("-c","--convert", help="Conversion format", action="store")
parser.add_argument("-m","--mixed", help="Input file contains multiple repeat types (UCSC output)", action="store_true")
parser.add_argument("-e","--fixedend", help="Sets each annotation end position to this value (DFAM output)", nargs=1, type=int)

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
if not args.convert:
    print("Conversion type required")
    error = 1

if error==1:
    print("\nAnnotation file converter requires an input file, output filename and conversion type.\n")
    sys.exit()

if args.convert.upper() not in ["BED", "DFAM", "UCSC", "GTF"]:
    print("\nAccepted conversion options are BED, GTF, DFAM or UCSC.\n")
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

repclass = "LINE"           # Value to use for the UCSC repClass field when converting from other formats
repfamily = "L1"            # Value to use for the UCSC repFamily field when converting from other formats
if args.mixed:
    repclass = NullString   # If the annotation file contains a mix of repeat types use the unknown value instead.
    repfamily = NullString

fixedend = None
if args.fixedend:
    fixedend=args.fixedend[0]

### Processing the conversion

processInput(args.input,args.output,type,args.convert.upper())
