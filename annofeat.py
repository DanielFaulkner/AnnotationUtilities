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
parser.add_argument("-m","--margin", help="Margin to include in basepairs [use with -o]", nargs=1, type=int)
parser.add_argument("-a","--all", help="List all features", action="store_true")
parser.add_argument("-t","--title", help="Column title [use with -o]", action="store")
parser.add_argument("-o","--overlap", help="Only examine overlapping region", action="store_true")
parser.add_argument("-s","--sense", help="Order closest items by sense and antisense", action="store_true")
parser.add_argument("-f","--features", help="Features to include when look for closest feature", action="store")

# Any commands entered without a flag
args = parser.parse_args()

# Setup variables:
features=['exon','transcript']

all = 0
if args.all:
    all = 1
    features=[]

margin = 0
if args.margin:
    margin = args.margin[0]

title = ""
if args.title:
    title = args.title

useoverlap = 0
if args.overlap:
    useoverlap = 1

usesense = 0
if args.sense:
    usesense = 1

if args.features:
    features=args.features.split(',')

# Run the command
print("Indexing reference file")
trackobj = libAnnoShared.loadTrackFile(args.reference)
print("Processing annotations *This may take some time if used with large unsorted files*")
if useoverlap:
    libAnnoFeat.featureOverlappingAddColumn(args.query,trackobj,args.output,margin,title,all)
else:
    libAnnoFeat.featureClosestAddColumn(args.query,trackobj,args.output,usesense, all, features)


# Close files
args.query.close()
args.reference.close()
args.output.close()
