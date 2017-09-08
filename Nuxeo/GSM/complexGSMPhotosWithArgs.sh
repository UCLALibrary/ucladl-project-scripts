#!/bin/bash

set -x
set -euo pipefail

nx ls /

remote=/asset-library/UCLA/uclalsc/goldenstate/box$1

for i in {001..23};
do
	id="uclalsc_1434_b$1_f"$i
	holder=${remote}/${id}
        for j in {001..134};
        do
		#photograph="$(ls ${id}_${j}.tif)"

		
                if [ -e ${id}_${j}.tif ]; then
		  nx mkdoc -f -t SampleCustomPicture ${holder}_${j}
                  nx upfile -dir ${holder}_${j} ${id}_${j}.tif 
		 	
                  
                fi 
                
                #back=$(ls ${id}_${j}a.tif)
                
                 if [ -e ${id}_${j}a.tif ]; then
                  nx mkdoc -f -t SampleCustomPicture ${holder}_${j}
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

