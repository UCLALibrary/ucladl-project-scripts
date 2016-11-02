#!/bin/bash

# This is a generic script for copying files from one directory to another.
# It is used like this:
#
# ./copy-file-list.sh filenames.txt /path/to/src/dir /path/to/dest/dir
#
# 1. filenames.txt must be a file that contains a list of filenames (not paths),
#    with one filename per line.
# 2. /path/to/src/dir and /path/to/dest/dir must not have trailing slashes.

i=1
for file in $(< $1);
do
    file=$(echo $file | tr -d '\r')
    cp $2/$file $3/$file && echo 'Moved '$file' '$i;
    i=$((i+1))
done
