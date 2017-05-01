xargs -I {} \
    nx upfile \
      -dir \
      /asset-library/UCLA/dawntest/[directory] \
      {} << HERE
image1
image2
HERE
