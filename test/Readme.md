# Available tests:
All tests are designed to work on Linux, minor modifications are likely to be required for use with other operating systems.

conversiontest.py
This python program calls the annoconv.py program from a terminal window and converts each of the provided files in the sampledata directory to every supported file type and save the result in a folder called convertedfiles.

filtertest.py
This python program calls the annofilter.py program from a terminal window and performs a set of predefined filtering options on a sampledata file. The results are saved in a folder called filteredfiles.

viewertest.py
This python program starts the annoview.py program using either the sample data or downloaded RefSeq data.

scriptexample.sh
A small example demonstrating how the filter and conversion utilties can be combined and used as part of an automated shell script. The results are saved in a folder called scriptoutput.


# Sample data license:

The sample dataset is based on real information available from the DFAM website (www.dfam.org). This data has been made available by DFAM under the Creative Commons Zero license. This data has then been converted into the other formats to form the initial test data using the annotation converter.

These files can be replaced with other sources for testing purposes, but for redistribution would need to be available under a permissive copyright.
