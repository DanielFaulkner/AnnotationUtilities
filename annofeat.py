#!/usr/bin/python3
# annofeat
#
# A terminal prompt interface to add columns detailing nearby feature to an annotation file.
#
# By Daniel R Faulkner

from lib import libAnnoFeat
from lib import libAnnoShared
import argparse

## Command line options:
### Parse the command line arguments
parser = argparse.ArgumentParser(description="Annotation, add overlapping feature column")
# Arguments:
# Required
parser.add_argument("query", help="Query filename", type=argparse.FileType('r'))
parser.add_argument("reference", help="Reference filename", type=argparse.FileType('r'))
parser.add_argument("output", help="Output filename", type=argparse.FileType('w'))
# Optional
parser.add_argument("-m","--margin", help="Basepair margin to include", nargs=1, type=int)
parser.add_argument("-a","--all", help="List all features", action="store_true")
parser.add_argument("-t","--title", help="Column title", action="store")
parser.add_argument("-c","--closest", help="List closest features regardless of distance", action="store_true")
parser.add_argument("-s","--sense", help="Order closest items by sense and antisense", action="store_true")

# Any commands entered without a flag
args = parser.parse_args()

# Setup variables:
all = 0
if args.all:
    all = 1

margin = 0
if args.margin:
    margin = args.margin[0]

title = ""
if args.title:
    title = args.title

useclosest = 0
if args.closest:
    useclosest = 1

usesense = 0
if args.sense:
    usesense = 1

# Run the command
print("Indexing reference file")
trackobj = libAnnoShared.loadTrackFile(args.reference)
if useclosest:
    libAnnoFeat.featureClosestAddColumn(args.query,trackobj,args.output,usesense, all)
else:
    print("Processing annotations *This may take some time*")
    libAnnoFeat.featureOverlappingAddColumn(args.query,trackobj,args.output,margin,title,all)

# Close files
args.query.close()
args.reference.close()
args.output.close()
