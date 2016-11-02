#!/bin/bash

# This is a generic script for verifying the existence of a list of files.
# It is used like this:
#
# ./verify-copy-file-list.sh filenames.txt /path/to/dir
#
# 1. filenames.txt must be a file that contains a list of filenames (not paths),
#    with one filename per line.
# 2. /path/to/dir must not have a trailing slash.

i=0
for file in $(< $1);
do
    if [ ! -e $2/$file ]
    then
        echo $2/$file 'does not exist'
    fi
done
