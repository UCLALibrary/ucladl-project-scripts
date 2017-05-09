#!/bin/bash
# this script will ingest the files under Box1 with the first loop going 
# through folder information in the file names
# and then finding photographs within that folder based again on the 
# file name 

set -x
set -u
set -e

nx ls /

remote=/asset-library/UCLA/uclalsc/miriammatthews/box01

for i in {01..17};
do
	id="uclalsc_1889_b01_f"$i
	holder=${remote}/${id}
        for j in {001..10};
        do

		
                if [ -e ${id}_${j}.tif ]; then
		  nx mkdoc -f -t SampleCustomPicture ${holder}_${j}
                  nx upfile -dir ${holder}_${j} ${id}_${j}.tif 
		 	
                  
                fi 
                
                # find if front and back exists
                
                 if [ -e ${id}_${j}a.tif ]; then
                  # create photograph object in Nuxeo
                  nx mkdoc -f -t SampleCustomPicture ${holder}_${j}
		  # find the images and upload them in Nuxeo
                  ls ${id}_${j}?.tif \
                    | xargs -I {} \
                  nx upfile -dir ${holder}_${j} {}
                fi

           		
        done

        #nx mkdoc -f -t SampleCustomPicture ${holder}
	#ls ${id}_????.tif \
	 #| xargs -I {} \
	#nx upfile -dir ${holder} {}
done

