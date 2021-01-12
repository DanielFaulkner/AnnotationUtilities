# Annotation Utilities userguide

The annotation utilities provides a few tools in aid in the manipulation and inspection of annotation files.

**Supported file types:**  
- BED
- UCSC Table browser
- DFAM
- GTF/GFF

All files must use tab separation and comments and headers must be indicated with a preceeding '#' character. Each utility will try to determine the filetype based on it's file extension or content. If a utility is unable to determine the file type of an input this can be corrected by changing the file extension to either .bed,.csc,.fam or .gtf. Alternatively it maybe possible to indicate this as an argument when starting a utility.

**Requirements:**  
Python (version 3) is required.  
These utilities have been written and tested in Linux, but may work with other operating systems with little or no modification.  

## Annotation converter (annoconv.py)

Converts an annotation file from one of the supported file formats to another. This should be avoided where possible as different formats permit different fields, therefore some information may not be converted or maybe stored in a comparable field. However, if your usecase requires some annotations to be converted between formats this utility can produce a basic conversion.

**Arguments:**  
-i/--input:	Input filename 			(required, filepath)  
-o/--output:	Output filename 		(required, filepath)  
-c/--convert:	File format to convert into 	(required, BED/GTF/DFAM/UCSC)  
-t/--type:	Input file type 		(optional, use if file format is not detected)  
-m/--mixed:	Indicates a mixed file type	(optional, only affects UCSC table browser output)  
-e/--fixedend:	Sets a fixed annotation size	(optional, only affects DFAM output)  

**Example:**  
Converting a DFAM formatted file into a BED formatted file.

python3 annoconv.py -i test/sampledata/DFAM.tsv -o BEDConversion.bed -c BED


## Annotation filter (annofilter.py)

Reads an annotation file, applying filters and saving the results under a new filename. Each filter can only be used once, if multiple filters of the same type are required this will require multiple uses of the utility. If using a regular expression filter refer to the python regular expression guide for information on how to form the filter.

**Arguments:**  
-i/--input:	Input filename 			(required, filepath)  
-o/--output:	Output filename 		(required, filepath)  
-t/--type:	Input file type 		(optional, use if file format is not detected)  
--score		Minimum score			(filter, requires integer value)  
--size		Minimum annotation size		(filter, requires integer value)  
--minpromoter	Minimum promoter size(bp)*	(filter, requires integer value)  
--reqregion	Required annotation region	(filter, requires 2 integer values)  
--orfs		File containing ORF positions*	(Used with minpromoter, filepath)  
--defaultend	Manually defined promoter end*	(Used with minpromoter, requires an integer value)  
--annonames	Filter for this filename**	(filter, requires string)  
--chrnames	Filter for this chromosome**	(filter, requires string)  
--exclude	Inverts name filters**		(modifier for annonames/chrnames)  
--regex		Indicates regular expression**	(modifier for annonames/chrnames)  

**Example:**  
Filtering a file to remove annotations below a score of 500 and with 100bp within the first 1000bps.

python3 annofilter.py -i test/sampledata/DFAM.tsv -o DFAMfiltered.tsv --minpromoter 100 --defaultend 1000 --score 500

Filtering a file to remove annotations which end in _alt.

python3 annofilter.py -i test/sampledata/DFAM.tsv -o DFAMfiltered.tsv --annonames \w*_alt --regex --exclude

## Annotation viewer (annoview.py)

There are many text editors and spreadsheet programs suitable for examining annotation files. This utility does not aim to compete with these, but instead provide a means to open two annotation files and compare their contents graphically to give an indication of an annotations relevance when viewed in context.

As gene annotations are available in GTF format this does facilitate the use of this utility as a very basic genome browser that can be used from within a terminal. However for a more detailed view an alternative software package or website would be required.

**Arguments:**  
Query filename		The annotation file to examine		(required, filepath)  
Reference filename	The annotation file for comparison	(required, filepath)  
-l/--line:		Query file line to view 		(optional)  
-z/--zoom:		Size of genomic region to view (bp)	(optional)  
-f/--features		Size of the nearby feature view		(optional)  

**Example:**  
Opening two annotation files containing repeat annotations for comparison.

python3 annoview.py test/sampledata/DFAM.tsv test/sampledata/GTF.gtf

Comparing a repeat file containing annotations to a genomic feature reference file. Starting at line 30 with a genomic region view of 50000bps.  

python3 annoview.py test/sampledata/DFAM.tsv hg38.ncbiRefSeq.gtf -z 50000 -l 30  

**Use:**  
This utility displays 3 sets of information, they are:
- Query file view: The query annotation information. The current line is indicated with a '*' and lines which extend beyond the screen end with '>'. This can show either the annotation information as it is stored within the file or an edited version with only a subset of the fields visible.
- Genomic region view: A representation of the genomic region centred on the line indicated in the Query file view. Exons are represented with a '#', transcripts with '-' and other features with '~'. The size of the region can be modified and the view can be configured to hide or show small features.
- Nearby features view: A list of nearby features in the format 'large feature':'start' 'end'-'feature' 'name' (ie. Y:10-1000 exon ABC1). The left column lists overlapping features and those preceeding while the right column lists following features, from closest to furthest.

Finally the display has a prompt where you can enter commands to interact with the view. Pressing enter or typing in an unknown command will cause the display to refresh, useful if the terminal window size has changed. Entering a number will change the active query line and recentre the view on that line. Typing 'help' will display a list of commands which can be used to interact with the view. These include:  

zoomin		Increases magnification of the genome window  
zoomout		Decreases magnification of the genome window  
viewall		Shows all items in the genome window (use viewall ref/query to specify a track)  
viewlarge	Hides items which are smaller than a character  
query r/l	Moves the query view to the right or left (if lines extend beyond the screen)  
query unedited	Shows the query annotations unedited  
query edited	Shows the query annotations in a standardised format  

## Useful resources
This section contains links to some useful resources applicable to both using the utilities and on where to find suitable annotation files.  

- Regular expression formatting from [Python documentation](https://docs.python.org/3/library/re.html)
- DFAM repeat annotation files from [DFAM's website](www.dfam.org)
- BED formatted annotation files from [UCSC's repeat browser](https://repeatbrowser.ucsc.edu/data/)
- GTF formatted genome annotation from [UCSC](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/genes/)
- GTF formatted genome annotation from [NCBI](https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/reference/GCF_000001405.39_GRCh38.p13/)
- UCSC repeat annotation files from [UCSC's table browser website](https://genome.ucsc.edu/cgi-bin/hgTables)

**UCSC Table browser settings:**  
Open Reading Frame (ORF) positions:  
Clade - UCSC Repeat Browser 2020 Update  
Genome - Human Repeats ; Assembly - Repeat Browser 2020  
Group - Annotations of Repeat Consensus ; Track - Consensus Annotations  
Table - hub_2090001_repNames ; Region - genome  
Output file - tbOrfAnnotations.tsv  

Repeat annotations:  
Clade - Mammal  
Genome - Human ; Assembly - Dec. 2013 (GRCh38/hg38)  
Group - Repeats ; Track - RepeatMasker  
Table - rmsk ; Region - genome  
Output file - UCSC.tsv  
