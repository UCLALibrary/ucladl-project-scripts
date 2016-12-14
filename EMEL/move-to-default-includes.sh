#!/bin/bash

# Move all image files and associated XMP files in each folio that contain
# certain substrings in their filenames to a default includes directory
# (inside each folio directory), and compile a list of all default included
# files for each manuscript.
#
#
# Usage:
#
#   ./move-to-default-includes.sh substring-list /dir/containing/manuscripts
#
#   1. substring-list is a text file (named anything) that contains a list of
#      substrings; files that contain them will be moved to a default_includes
#      folder (one folder for each folio) and added to the listfile of included
#      files (one such file per manuscript)
#
#   2. The path to the directory that contains manuscripts should not end with
#      a slash
#
#
# In other words, provided a file that contains a newline-separated list of substrings:
#
#   aaa
#   ccc
#
# the directory structure goes from:
#
#   manuscript1/
#     folio1/
#       image1aaa.tif
#       image1aaa.tif.xmp
#       image1bbb.tif
#       image1bbb.tif.xmp
#       image1ccc.tif
#       image1ccc.tif.xmp
#     folio2/
#       image2aaa.tif
#       image2aaa.tif.xmp
#       image2ccc.tif
#       image2ccc.tif.xmp
#       image2ddd.tif
#       image2ddd.tif.xmp
#
# to:
#
#   manuscript1/
#     manuscript1_includes.csv
#     folio1/
#       default_includes/
#         image1aaa.tif
#         image1aaa.tif.xmp
#         image1ccc.tif
#         image1ccc.tif.xmp
#       image1bbb.tif
#       image1bbb.tif.xmp
#     folio2/
#       default_includes/
#         image2aaa.tif
#         image2aaa.tif.xmp
#         image2ccc.tif
#         image2ccc.tif.xmp
#       image2ddd.tif
#       image2ddd.tif.xmp
#
# where manuscript1_includes.csv has the contents:
#
#   image1aaa
#   image1ccc
#   image2aaa
#   image2ccc
#
#
# IMPORTANT:
#
# If new manuscripts are added, new folios are added to a manuscript, new
# images added to a folio directory, or new substrings (algorithms) are added
# to substring-list, then just run this script again.
#
# However, if one or more folios with included images, or included images
# themselves, are removed from the directory structure, or if one or more
# substrings are removed from the substrings file, then it would be best to
# run 'undo-move-to-default-includes.sh' first to make sure everything is in
# sync, then re-run this script.

if [ ! -e $1 ]
then
    echo $1 'does not exist!'
    exit 1
fi

EXTRACT_BASENAME_REGEXP='s/^.*\///g'

SUBSTRINGS=$(tr -d '\r' < $1)
MANUSCRIPTS_DIR=$2
MANUSCRIPT_DIRS=$(find ${MANUSCRIPTS_DIR} -mindepth 1 -maxdepth 1 -type d)

for manuscript_dir in ${MANUSCRIPT_DIRS}
do
    MANUSCRIPT_DIR_BASENAME=$(echo ${manuscript_dir} | sed -e ${EXTRACT_BASENAME_REGEXP})
    DEFAULT_INCLUDED_FILE=${manuscript_dir}/${MANUSCRIPT_DIR_BASENAME}_includes.csv
    TMP_DEFAULT_INCLUDED_FILE=${manuscript_dir}/tmp_default_included

    # make sure default_included.txt exists

    touch ${DEFAULT_INCLUDED_FILE}

    # remove any relative paths from DEFAULT_INCLUDED_FILE

    sed -e ${EXTRACT_BASENAME_REGEXP} ${DEFAULT_INCLUDED_FILE} > ${TMP_DEFAULT_INCLUDED_FILE}

    # record matches in all the folio dirs

    FOLIO_DIRS=$(find ${manuscript_dir} -mindepth 1 -maxdepth 1 -type d)
    for folio_dir in ${FOLIO_DIRS}
    do
        DEFAULT_INCLUDES_DIR=${folio_dir}/default_includes
        mkdir ${DEFAULT_INCLUDES_DIR}

        for substring in ${SUBSTRINGS}
        do
            # move all files in the curent subdirectory that contain 'substring'
            # in the filename to 'default_includes' (both images and metadata)

            MATCHING_FILES=$(find ${folio_dir} -mindepth 1 -maxdepth 1 -type f \
                -name '*'${substring}'*')

            if [[ ${MATCHING_FILES} != '' ]]
            then
                mv --target-directory=${DEFAULT_INCLUDES_DIR} ${MATCHING_FILES}

                # write image file names (not paths) to tmp

                echo ${MATCHING_FILES} \
                    | sed -e 's/ \+/\n/g' \
                    | sed -e '/^.*\.xmp$/d' \
                    | sed -e ${EXTRACT_BASENAME_REGEXP} \
                    >> ${TMP_DEFAULT_INCLUDED_FILE}
            fi
        done
    done

    # add new filenames to DEFAULT_INCLUDED_FILE

    sort -u ${TMP_DEFAULT_INCLUDED_FILE} > ${DEFAULT_INCLUDED_FILE}

    # remove tmp file

    rm ${TMP_DEFAULT_INCLUDED_FILE}
done
