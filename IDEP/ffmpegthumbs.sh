# ffmpeg script to generate 5 thumbnails per video.
# Create a "thumbs" directory within the directory containing the video files.
# Add this file to "thumbs" directoy and run script from there

for file in ../*.mp4; do
  filename=$(basename "$file");
  filename=${filename%.*};
  ffmpeg -i "$file" -ss 3 -pix_fmt yuv420p -vf "select=gt(scene\,0.4),scale=iw*min(256/iw\,256/ih):ih*min(256/iw\,256/ih), pad=256:256:(256-iw*min(256/iw\,256/ih))/2:(256-ih*min(256/iw\,256/ih))/2" -frames:v 5 -vsync vfr "${filename}_thumb_%02d.jpg"; 
  
  if [ ! -f $filename"_thumb0_1.jpg" ]; then 
    ffmpeg -i $file -ss 3 -pix_fmt yuv420p -vf "thumbnail,scale=iw*min(256/iw\,256/ih):ih*min(256/iw\,256/ih), pad=256:256:(256-iw*min(256/iw\,256/ih))/2:(256-ih*min(256/iw\,256/ih))/2" -frames:v 1 "${filename}_thumb_01.jpg" -n;
  fi;
done
