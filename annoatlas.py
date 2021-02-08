#!/usr/bin/python3
# annoatlas
#
# A terminal prompt interface to combine an annotation file with a Human Protein Atlas dataset
#
# By Daniel R Faulkner

from lib import libAnnoAtlas
from lib import libAnnoShared
import argparse

## Command line options:
### Parse the command line arguments
parser = argparse.ArgumentParser(description="Combine annotation and Human Protein Atlas datasets")
# Arguments:
# Required
parser.add_argument("input", help="Annotation filename", type=argparse.FileType('r'))
parser.add_argument("atlas", help="Human Protein Atlas filename", type=argparse.FileType('r'))
parser.add_argument("output", help="Output filename", type=argparse.FileType('w'))
# Optional
parser.add_argument("-c","--column", help="Feature name column (annotation file)", nargs=1, type=int)
parser.add_argument("-r","--regex", help="Use regular expression string matching", action="store_true")
parser.add_argument("-a","--atlascols", help="Human Protein Atlas columns to include", action="store")

# Any commands entered without a flag
args = parser.parse_args()

regex = 0
if args.regex:
    regex = 1

GeneCol = -1
if args.column:
    GeneCol = args.column[0]

atlasCol = []
if args.atlascols:
    atlasCol = args.atlascols.split(',')

# Run the command
libAnnoAtlas.combineEntries(args.input,args.atlas,args.output, atlasCol, regex, GeneCol)

# Close files
args.input.close()
args.atlas.close()
args.output.close()
