#!/usr/local/bin/python

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