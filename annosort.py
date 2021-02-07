#!/usr/bin/python3
# annosort
#
# A terminal prompt interface to sort entries within an annotation file.
#
# By Daniel R Faulkner

from lib import libAnnoSort
from lib import libAnnoShared
import argparse

## Command line options:
### Parse the command line arguments
parser = argparse.ArgumentParser(description="Sort annotation file by genomic position")
# Arguments:
# Required
parser.add_argument("input", help="Input filename", type=argparse.FileType('r'))
# Optional
parser.add_argument("-o","--output", help="Output filename", type=argparse.FileType('w'))
parser.add_argument("-s","--status", help="View current sort status", action="store_true")

# Any commands entered without a flag
args = parser.parse_args()

# Run the command
print("Indexing reference file")
trackobj = libAnnoShared.loadTrackFile(args.input)
if args.status:
    # Display the current status of the annotation file
    sortstr = "NO"
    orderstr = "NO"
    if trackobj.ordered:
        orderstr = "YES"
    if trackobj.sorted:
        sortstr = "YES"
    print("Annotation file grouped by chromosome: "+orderstr)
    print("Annotation file sorted by start position: "+sortstr)
elif args.output:
    # Sort the file
    libAnnoSort.sort(trackobj,args.output)
else:
    print("Status [-s] or Output filename [-o] option required")

# Close files
args.input.close()
if args.output:
    args.output.close()
