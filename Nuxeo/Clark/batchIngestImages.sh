# Batch ingest images from a directory that shares the same name as the folder or folderish object in Nuxeo.
# "${PWD##*/}" prints the current directory w/out path.
# Used for Clark manuscripts.
# Imports all .tif files in the directory.
# Should be run from the same directory as the files. 
# For similar collections, replace "clark/mss" with appropriate path.

filelist=$(find ./ -type f -name '*.tif' | cat | sort)
echo $filelist

xargs -I {} \
    nx upfile \
      -dir \
      /asset-library/UCLA/clark/mss/"${PWD##*/}" \
       {} << HERE
$filelist
HERE
