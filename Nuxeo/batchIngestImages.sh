
filelist=$(ls *.tif)
set -euo pipefail

xargs -I {} \
    nx upfile \
      -dir \
      /asset-library/UCLA/dawntest/[directory] \
       {} << HERE
$filelist
HERE
