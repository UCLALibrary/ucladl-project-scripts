#!/bin/bash

# This script undoes 'move-to-default-includes.sh':
#   1. Deletes the default_included file
#   2. Moves all files out of the default_includes directories and back into
#      their folio directory
#   3. Deletes all (empty) default_includes directories
#
# Usage:
#
#   ./undo-move-to-default-includes.sh /dir/containing/manuscripts
#
#   1. The path of the directory containing manuscripts must not end in a slash

MANUSCRIPTS_DIR=$1
MANUSCRIPT_DIRS=$(find ${MANUSCRIPTS_DIR} -mindepth 1 -maxdepth 1 -type d)

for manuscript_dir in ${MANUSCRIPT_DIRS}
do
    MANUSCRIPT_DIR_BASENAME=$(echo ${manuscript_dir} | sed -e 's/^.*\///g')
    DEFAULT_INCLUDED_FILE=${manuscript_dir}/${MANUSCRIPT_DIR_BASENAME}_includes.csv
    rm ${DEFAULT_INCLUDED_FILE}

    FOLIO_DIRS=$(find ${manuscript_dir} -mindepth 1 -maxdepth 1 -type d)
    for folio_dir in ${FOLIO_DIRS}
    do
        DEFAULT_INCLUDES_DIR=${folio_dir}/default_includes
        mv ${DEFAULT_INCLUDES_DIR}/* ${folio_dir}
        rmdir ${DEFAULT_INCLUDES_DIR}
    done
done
