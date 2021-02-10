# Annotation Utilities userguide

The annotation utilities provides a few tools in aid in the manipulation and inspection of annotation files.

**Supported file types:**  
- BED
- UCSC Table browser
- DFAM
- GTF/GFF

All files must use tab separation and comments and headers must be indicated with a preceding '#' character. Each utility will try to determine the file type based on it's file extension or content. If a utility is unable to determine the file type of an input this can be corrected by changing the file extension to either .bed,.csc,.fam or .gtf. Alternatively it maybe possible to indicate this as an argument when starting a utility.

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

## Annotation tabulate (annotabify.py)

Converts a GTF/GFF formatted file into a standard, TSV, tab separated file. The resulting file should be suitable for spreadsheet or statistics packages which do not support GTF's mix of tab and semicolon separated fields.
If the output is saved as a .gtf file the output is still recognised by these utilities. This operation can be undone using the -r/--reverse option to store any modifications which have been made in the GTF format.

**Arguments:**  
Input filename 			(required, filepath)  
Output filename 		(required, filepath)  
-r/--reverse:	Reverses the tabulation function to convert back to a standard GTF format.  
-t/--header:	Include the header line [0-No, 1-If present, 2-Yes]. Default is 1.  

**Example:**  
Tabulating a GTF file so all fields are separated by tab characters.

python3 annotabify.py test/sampledata/GTF.gtf GTFtabulated.gtf

## Annotation sorter (annosort.py)

This utility checks the order of annotation entries within a file and can either show the status of the file using the -s/--status option or if an output file is provided using the -o/--output option sort the file. The entries are grouped by chromosome, alphabetically, and sorted by the alignment start positions.

**Arguments:**  
Input filename 			(required, filepath)  
-o/--output:	Output file name to use.  
-s/--status:	View the current sort status of the annotation file.  

**Example:**  
Sort an annotation file.

python3 annosort.py test/sampledata/GTF.gtf -o sortedfile.gtf

View the sort status of an annotation file.

python3 annosort.py test/sampledata/GTF.gtf -s

## Annotation closest/overlapping feature (annofeat.py)

This utility reads an annotation file and looks for features in a reference annotation file which are nearby or overlap. These are then added as additional tab separated columns in the output.  
The utility has two modes, the default detection method returns the closest features before and following an annotation as well as those overlapping. The features to include when looking for the closest feature can be provided as a comma separated list using the -f/--features option. This adds columns to the annotation file for the closest feature type, name, strand and distance from annotation, in each direction and within.  
The alternative method detects only features overlapping an annotation, although this region can be extended to include neighbouring features with the -m/--margins option. This adds columns for overlapping feature types and feature names to the annotation file.  
The output can be configured to return all results using the -a/--all option or just those with the highest priority. The default option is to only include transcripts and exons. This can be modified, see comments in libAnnoFeat.py file for instructions on how to modify the priority list.
This utility can compare any two support annotation files but is most likely to be used to compare the results of an analysis against a genome annotation file.  
NOTE: This utility will run significantly slower with files which are not sorted by genomic position.  

**Arguments:**  
Query filename 			(required, filepath)  
Reference filename  (required, filepath)  
Output filename 		(required, filepath)  
-m/--margin:  Additional margin (in bps) to include in the search for overlapping features (use with -o).  
-a/--all:       Returns all overlapping features as a semicolon separated list.  
-t/--title:     Title to use for the column header, if a header line is present (use with -o).  
-o/--overlap:   Only returns those results which overlap with an annotation.
-s/--sense:     Return the results formatted using sense/antisense direction.
-f/--features:  Features to include when looking for the closest feature.

**Example:**  
Searching for overlapping features + 10 base pairs with itself, an unrealistic use case.

python3 annofeat.py test/sampledata/GTF.gtf test/sampledata/GTF.gtf output.gtf -o -a -t OverlappingPlus10 -m 10

Searching for closest transcripts, exons and UTR features using a hypothetical genome annotation file.

python3 annofeat.py test/sampledata/GTF.gtf genefeatures.gtf output.gtf -a -f transcript,exon,UTR

## Annotation atlas (annoatlas.py)

This utility adds columns from a Human Protein Atlas dataset to an annotation file. If the annotation file format does not include gene names by standard this can be defined manually using the -c/--column option, starting at column 0. The columns to add from the Human Protein Atlas dataset can be defined using the -a/--atlascols option. This option supports a comma separated list of column numbers, column names or regular expression search terms, with the -r/--regex option.  
NOTE: Only the TSV formatted complete dataset is compatible. The gene name, synonym and Ensembl ID columns are used for detecting a match with an annotation file entry.

**Arguments:**  
Input filename 			(required, filepath)  
Atlas filename 			(required, filepath)  
Output filename 		(required, filepath)  
-c/--column:    Annotation file column containing gene names.  
-r/--regex:	    Use regular expression search terms for atlas columns.  
-a/--atlascols: Human Protein Atlas columns to add to the annotation file.

**Example:**  
Add specific columns to an annotation file.

python3 annoatlas.py test/sampledata/atlastest.bed proteinatlas.tsv combinedoutput.tsv -c 6 -a 6,7,Chromosome

Add columns containing the word RNA based using a regular expression search term.

python3 annoatlas.py test/sampledata/atlastest.bed proteinatlas.tsv combinedoutput.tsv -c 6 -a RNA -r

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

## Example project
This section includes a short example project using these tools to identify how many annotations have a, potentially, intact promoter and follow a prognostic proteins.  
Required files:
- Human Protein Atlas as proteinatlas.tsv
- NCBI Reference Sequence annotation as hg38.gtf
- Annotation file as DFAM.tsv

First filter the annotation file to find features with an intact promoter.
- python3 annofilter.py -i DFAM.tsv -o DFAMfiltered.tsv --minpromoter 100 --defaultend 1000

Convert the file to a GTF file (not needed, but here as an example)
- python3 annoconv.py -i DFAMfiltered.tsv -o GTFfiltered.gtf -c GTF

To speed up comparisons between feature files ensure NCBI reference annotation is sorted by genomic position.
- python3 annosort.py hg38.gtf -o hg38sorted.gtf

Convert the annotation file to a standard tsv format.
- python3 annotabify.py GTFfiltered.gtf GTFtabulated.gtf

Add information on the closest feature
- python3 annofeat.py GTFtabulated.gtf hg38sorted.gtf GTFfeatures.gtf -s

Add columns from the Human Protein Atlas dataset
- python3 annoatlas.py GTFfeatures.gtf proteinatlas.tsv GTFatlas.gtf -c 13 -a Pathology -r

Convert back to a standard GTF formated file
- python3 annotabify.py GTFatlas.gtf GTFdetabulated.gtf -r


At the end of these commands the GTF file should contain information on the closest features and relevant prognostic information. This can then be sorted or filtered in a spreadsheet software package, using the GTFatlas.gtf file as a TSV file type, or fed into further analysis software.    
NOTE: When adding columns to annotation files it is important to preserve the header and file extensions if the file is to be used by another utility, so the software recognises which columns contain essential information.

## Useful resources
This section contains links to some useful resources applicable to both using the utilities and on where to find suitable annotation files.  

- Regular expression formatting from [Python documentation](https://docs.python.org/3/library/re.html)
- DFAM repeat annotation files from [DFAM's website](www.dfam.org)
- BED formatted annotation files from [UCSC's repeat browser](https://repeatbrowser.ucsc.edu/data/)
- GTF formatted genome annotation from [UCSC](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/genes/)
- GTF formatted genome annotation from [NCBI](https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/reference/GCF_000001405.39_GRCh38.p13/)
- UCSC repeat annotation files from [UCSC's table browser website](https://genome.ucsc.edu/cgi-bin/hgTables)
- The Human Protein Atlas dataset from [The Human Protein Atlas website](https://www.proteinatlas.org/about/download)

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
