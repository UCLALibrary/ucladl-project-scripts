#this script has the following assumption built in:
####The filename column is in the first column in both spreadsheets.  
####If they are not this script will not work.  
#It also takes out the filename column from the metadata spreadsheet
#This script works in both python3 and python2
#the output spreadsheet will save to the same place as the script

import csv
import os

try:
    filelist = raw_input("Enter the filepath with filenaame of file list csv: ") #python2
except:
    filelist = input("Enter the filepath with filenaame of file list csv: ") #python3

try:
    metadata = raw_input("Enter the filepath with the filename name of metadata csv: ")
except:
    metadata = input("Enter the filepath with the filename name of metadata csv: ")

try:
    output = raw_input("Enter name of output file (exclude extension): ")
except:
    output = input("Enter name of output file (exclude extension): ")

filename = "{}.csv".format(output)

f1 = open(os.path.relpath(filelist), 'r') #open files
f2 = open(os.path.relpath(metadata), 'r') #open metadata

combine = []
filereader = csv.reader(f1)
metadatareader = csv.reader(f2)
headers = next(metadatareader)

filelist2 = list(filereader)

for metadata in metadatareader:
    for files in filelist2:
        if metadata[0] in files[0]: #if metadata in column 1 is in filenames in column 1
            new_row = files + metadata[1:] #new row equals filename and metadata from column 2 onward
            combine.append(new_row) #add to row list

           
with open(filename, 'w') as csvfile: #write row list to csv file
    writer = csv.writer(csvfile)
    writer.writerows([headers])
    writer.writerows(combine)


                            
