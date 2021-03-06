# Batch ingest images from a directory that shares the same name as the folder or folderish object in Nuxeo.
# "${PWD##*/}" prints the current directory w/out path.
# Used for Clark manuscripts.
# Imports all .tif files in the directory.
# Should be run from the same directory as the files.
# For similar collections, replace "clark/mss" with appropriate path.

<<<<<<< HEAD
=======
# Batch ingest images from a directory that shares the same name as the folder or folderish object in Nuxeo.
# "${PWD##*/}" prints the current directory w/out path.
# Used for Clark manuscripts.
# Imports all .tif files in the directory.
# Should be run from the same directory as the files.
# For similar collections, replace "clark/mss" with appropriate path.

>>>>>>> b4ef5892cbdb8747414ac708457daeb25e55e754
#! /bin/bash
set -e
set -o pipefail

xargs -I {} \
    nx upfile \
      -dir \
      /asset-library/UCLA/clark/mss/"${PWD##*/}" \
       {} < ls *.tif
