objects=$(find ./ -type d)
echo $objects

xargs -I {} \
  nx \
    mkdoc \
    -t SampleCustomPicture \
    /asset-library/UCLA/clark/mss/{} << HERE
$objects
HERE