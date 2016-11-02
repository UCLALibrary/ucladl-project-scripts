#!/bin/bash

# Move all image files and associated XMP files in each folio that contain
# certain substrings in their filenames to a new subdirectory called
# 'default includes', and compile a list of all files that were moved for each
# manuscript.
#
# In other words, provided a file that contains a newline-separated list of substrings:
#
#   aaa
#   ccc
#
# the filesystem like goes from:
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
