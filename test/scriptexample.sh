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
echo
echo Expanding the gtf file so all columns are separated by a tab
python3 ../annotabify.py scriptoutput/convertedfile.gtf scriptoutput/tabbifiedfile.gtf -t 1
echo
echo Adding closest feature columns to the annotation file. Comparing to itself. Treating file as gtf formatted for purpose of parsing the file.
python3 ../annofeat.py scriptoutput/tabbifiedfile.gtf scriptoutput/tabbifiedfile.gtf scriptoutput/closestfeatures.gtf -a
