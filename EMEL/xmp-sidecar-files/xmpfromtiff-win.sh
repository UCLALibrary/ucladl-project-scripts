#!/bin/bash

# Script to batch generate XMP sidecar files from a folder of TIFFs

# If reading files on NetApp, include the full path
# starting with "\\svm_dlib\…"

echo Enter path to images:
read pathtoimages

echo Enter path to XMP:
read pathtoxmp

exiftool -ext tif -o $pathtoxmp/"%f.tif.xmp" $pathtoimages
