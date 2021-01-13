#!/usr/bin/python3
# annotabify
#
# A terminal prompt interface to tabulate GTF/GFF files
#
# By Daniel R Faulkner

from lib import libAnnoTabify
import argparse

## Command line options:
### Parse the command line arguments
parser = argparse.ArgumentParser(description="GTF/GFF Annotation Tabulator")
# Arguments:
# Required
parser.add_argument("input", help="Input filename", type=argparse.FileType('r'))
parser.add_argument("output", help="Output filename", type=argparse.FileType('w'))
# Optional
parser.add_argument("-r","--reverse", help="Convert back to GTF format", action="store_true")
parser.add_argument("-t","--header", help="Include column titles <0-No, 1-If present, 2-Yes>", nargs=1, type=int)

# Any commands entered without a flag
args = parser.parse_args()

# Setup variables:
header = 1
if args.header:
    header=args.header[0]

# Run the command
if args.reverse:
    libAnnoTabify.deTabify(args.input,args.output,header)
else:
    libAnnoTabify.Tabify(args.input,args.output,header)
