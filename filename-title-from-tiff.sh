#!/usr/local/bin/bash

# Extract the source file path to column A and title metadata to column B
echo Path to MS directory:
read pathToMSDirectory
echo Output filename without an extension or spaces:
read pathToCSV
exiftool -csv -Title $pathToMSDirectory > $pathToCSV".csv"

# Sort rows of CSV and save the output to a new/final CSV
sort -k1 -n -t, $pathToCSV".csv" > $pathToCSV"_final.csv"

# Delete the first CSV
rm $pathToCSV".csv"

# Remove the first 4 rows (the sample shots) from the CSV
sed -i '' 1,4d $pathToCSV"_final.csv"

# Remove the last row (the header row, now last after sort)
sed -i '' '$d' $pathToCSV"_final.csv"

# Truncate the file path with only filenames left in column A
sed -i '' 's:^\/.*sld:sld:' $pathToCSV"_final.csv"

# Remove "MS name" (not the directory name) as recorded in TIFF header, e.g. Sinai Arabic 14, from title in column B
echo MS name as recorded in TIFF header to be removed:
read MSname
sed -i "" "s:$MSname:f.:" $pathToCSV"_final.csv"
