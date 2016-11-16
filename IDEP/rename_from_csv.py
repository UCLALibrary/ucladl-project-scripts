#!/usr/local/bin/python


# Usage
#
#  $ python rename_from_csv.py
#
#  1. Assumes you have a file "rename.csv" with two columns. Column one is old filename, column two is new filename.
#  2. "rename.csv" should be in the parent folder
#  3. This file ("rename_from_csv.py") should be in the folder with the files to be renamed
#
#  Example directory structure:
#
#  project/
#      rename.csv
#      filestorename/
#          file1.tif
#          file2.tif
#          rename_from_csv.py

import os, csv, sys

with open('../rename.csv','rb') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
       oldname = row[0]
       if os.path.exists(oldname):
           newname = row[1]
           os.rename(oldname, newname)
           print >> sys.stderr, "renamed '%s' to '%s'" % (oldname, newname)
       else:
           print >> sys.stderr, "file '%s' not found" % oldname