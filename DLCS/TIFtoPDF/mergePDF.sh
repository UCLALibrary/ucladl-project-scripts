#!/bin/bash

set -x
set -u
set -e

#for N in {0001..1078..100}: do
#    eval gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=Part$N "files{$N..$((N+99))}" 
#echo "TESTING$N" #"files{$N..$((N+99))}"
#done

for value in {0801..1078..100}
do
	#echo $value
   eval gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=merged${value}.pdf "0491_{$value..$((10#$value+99))}.tif.pdf"
done

echo All done
