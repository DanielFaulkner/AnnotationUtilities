# AnnotationUtilities
Often annotation files require some preprocessing to make them suitable for use with an analysis package, or additional context to make sense of the results. These utilities may improve suitable workflows by performing some common annotation manipulation tasks from the terminal prompt.

Utilities:
- Annotation Converter - Converts key fields between different annotation file types.
- Annotation Filter - Filters annotations using a variety of criteria.
- Annotation Tabulator - Converts a GTF/GFF file from using both tab and semicolon separators to only tab characters.
- Annotation Features - Compares two annotation files and adds columns detailing overlapping features.
- Annotation Viewer - Compares two annotation files and displays a genomic representation of their positions.
- Annotation Sorter - Sorts entries in an annotation file by position.
- Annotation Atlas - Adds columns from The Human Protein Atlas dataset to an annotation file.

Combined these utilities should enable an annotation file to be filtered and converted into a format suitable for further analysis. Any interesting annotations can then be formatted to include details on overlapping/nearby features or viewed alongside another annotation file. This can be particularly useful when used with a genomic reference sequence annotation file.

Supported file formats are: BED, GTF/GFF, DFAM and UCSC Table browser downloads.

The 'doc' folder contains documentation on the use of these utilities and the 'test' folder contains some basic automated tests and examples.

**NOTE:** While care has been made to remove errors the outputs of these utilities come with no guarantee of accuracy. Please check the outputs of these utilities are accurate and suitable before using in research or production settings.

## Requirements
- Python, version 3
- Linux - however other operating systems may work with little or no modification needed.

## Author

These utilities for working on annotation files were written by Daniel Rowell Faulkner.
