echo These utilities can be included as part of a larger workflow using simple terminal scripting.
echo
echo The results of this example will be saved in the scriptoutput folder
mkdir scriptoutput
echo
echo Filtering to remove all entries with less than 100 bases in the promoter.
python3 ../annofilter.py -i sampledata/DFAM.tsv -o scriptoutput/filteredfile.tsv --minpromoter 100 --defaultend 1000
echo
echo Converting the results to the gtf file format
python3 ../annoconv.py -i scriptoutput/filteredfile.tsv -o scriptoutput/convertedfile.gtf -c GTF
