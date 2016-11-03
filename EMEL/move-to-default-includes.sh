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
# the filesystem goes from:
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
#     default_included.txt
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
# where default_included.txt has the contents:
#
#   image1aaa
#   image1ccc
#   image2aaa
#   image2ccc

if [ ! -e $1 ]
then
    echo $1 'does not exist!'
    exit 1
fi

SUBSTRINGS=$(tr -d '\r' < $1)
MANUSCRIPTS_DIR=$2
MANUSCRIPT_DIRS=$(find ${MANUSCRIPTS_DIR} -mindepth 1 -maxdepth 1 -type d)

for manuscript_dir in ${MANUSCRIPT_DIRS}
do
    DEFAULT_INCLUDED_FILE=${manuscript_dir}/default_included.txt 
    TMP_DEFAULT_INCLUDED_FILE=${manuscript_dir}/tmp_default_included

    # make sure default_included.txt exists
    touch ${DEFAULT_INCLUDED_FILE}
    touch ${TMP_DEFAULT_INCLUDED_FILE}

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

                # write image file names to tmp

                echo ${MATCHING_FILES} \
                    | sed -e 's/ \+/\n/g' \
                    | sed -e '/^.*\.xmp$/d' \
                    >> ${TMP_DEFAULT_INCLUDED_FILE}
            fi
        done
    done

    # add new filenames to DEFAULT_INCLUDED_FILE

    cat ${DEFAULT_INCLUDED_FILE} ${TMP_DEFAULT_INCLUDED_FILE} \
        | sort -u \
        | tee ${DEFAULT_INCLUDED_FILE}

    # remove tmp file

    rm ${TMP_DEFAULT_INCLUDED_FILE}
done
