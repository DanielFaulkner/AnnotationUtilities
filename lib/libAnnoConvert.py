# libAnnoConvert
# Functions to convert between different annotation formats
#
# By Daniel R Faulkner

from lib.libAnnoShared import columnnum

## Conversion functions

def BEDline(annoobj):
    """Constructs a BED entry from the common element"""
    entry = annoobj.chrName+"\t"+str(annoobj.alignStart)+"\t"+str(annoobj.alignEnd)+"\t"+annoobj.repName+"\t"+str(annoobj.score)+"\t"+annoobj.strand+"\n"
    return entry

# Repclass and repfamily can be set to "LINE" and "L1" respectively if all entries relate to L1 elements.
def UCSCline(annoobj, repclass=None, repfamily=None, fixedstart=None, fixedend=None):
    """Constructs a UCSC table browser entry from the common element"""
    if not repclass:
        repclass = annoobj.NullString
    if not repfamily:
        repfamily = annoobj.NullString
    entry = str(annoobj.NullInt)+"\t"+str(annoobj.score)+"\t"+str(annoobj.NullInt)+"\t"+str(annoobj.NullInt)+"\t"+str(annoobj.NullInt)+"\t"+annoobj.chrName+"\t"+str(annoobj.alignStart)+"\t"+str(annoobj.alignEnd)+"\t"+str(annoobj.getChrLeft())+"\t"+annoobj.strand+"\t"+annoobj.repName+"\t"+repclass+"\t"+repfamily+"\t"+str(annoobj.getMatchStart53())+"\t"+str(annoobj.matchEnd)+"\t"+str(annoobj.getMatchLeft53())+"\t"+str(annoobj.NullInt)+"\n"
    return entry

# NOTE: The NullInt variable affects the E-value score. Ignore this field in the converted file.
def DFAMline(annoobj, fixedend=None):
    """Constructs a DFAM entry from the common element"""
    # NOTE: Fixed end does not adjust the alignend value.
    if fixedend:
        repSize = fixedend
    else:
        repSize = annoobj.repSize
    # Construct entry
    entry = annoobj.chrName+"\t"+annoobj.NullString+"\t"+annoobj.repName+"\t"+str(annoobj.score)+"\t"+str(annoobj.NullInt)+"\t"+str(annoobj.matchStart)+"\t"+str(annoobj.matchEnd)+"\t"+str(repSize)+"\t"+annoobj.strand+"\t"+str(annoobj.getAlignStart53())+"\t"+str(annoobj.getAlignEnd53())+"\t"+str(annoobj.getAlignStart53())+"\t"+str(annoobj.getAlignEnd53())+"\t"+str(annoobj.chrSize)+"\n"
    return entry

def GTFline(annoobj, featureasrepName=1):
    """Constructs a GTF entry from the common element"""
    if featureasrepName:
        # Compulsory fields:
        gtftemplate="{}\tAnnotationConverter\t{}\t{}\t{}\t{}\t{}\t.\t"
        gtfstring=gtftemplate.format(annoobj.chrName,annoobj.repName,annoobj.alignStart,annoobj.alignEnd,annoobj.score,annoobj.strand)
        # Optional fields: (Available: repName,repSize,chrSize,matchStart,matchEnd)
        gtfextratemplate='repID "{}"; repSize {}; chrSize {}; matchStart {}; matchEnd {}\n'
        gtfextrastring=gtfextratemplate.format(annoobj.repID, annoobj.repSize,annoobj.chrSize,annoobj.matchStart,annoobj.matchEnd)
    else:
        # Compulsory fields:
        gtftemplate="{}\tAnnotationConverter\tAnnotation\t{}\t{}\t{}\t{}\t.\t"
        gtfstring=gtftemplate.format(annoobj.chrName,annoobj.alignStart,annoobj.alignEnd,annoobj.score,annoobj.strand)
        # Optional fields: (Available: repName,repSize,chrSize,matchStart,matchEnd)
        gtfextratemplate='repID "{}"; repName "{}"; repSize {}; chrSize {}; matchStart {}; matchEnd {}\n'
        gtfextrastring=gtfextratemplate.format(annoobj.repID, annoobj.repName,annoobj.repSize,annoobj.chrSize,annoobj.matchStart,annoobj.matchEnd)
    entry = gtfstring+gtfextrastring
    return entry

# Function to write file headers
def writeHeader(fileoutobj, type):
    DFAMHeader = "#sequence name\tmodel accession\tmodel name\tbit score\te-value\thmm start\thmm end\thmm length\tstrand\talignment start\talignment end\tenvelope start\tenvelope end\tsequence length\n"
    UCSCHeader = "#bin\tswScore\tmilliDiv\tmilliDel\tmilliIns\tgenoName\tgenoStart\tgenoEnd\tgenoLeft\tstrand\trepName\trepClass\trepFamily\trepStart\trepEnd\trepLeft\tid\n"
    GTFHeader = "#Chr\tSource\tFeature\tStart\tEnd\tScore\tStrand\tFrame\tOther attributes\n"
    if type=="DFAM":
        fileoutobj.write(DFAMHeader)
    elif type=="UCSC":
        fileoutobj.write(UCSCHeader)
    elif type=="GTF":
        fileoutobj.write(GTFHeader)
