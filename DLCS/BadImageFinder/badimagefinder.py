import sys
import os
from PIL import Image
from PIL import UnidentifiedImageError
import csv
from datetime import datetime

#helper function to try the most common corruption tests
def isCorrupt(img, path):
    if os.stat(path).st_size == 0:
        return True, "Zero file size"
    elif img.verify() is not None:
        return True, "Pillow verification failed"
    elif img.filename[-3:] == "tif" and Image.MIME[img.format] != "image/tiff":
        return True, "Non-TIFF MIME type for .tif file"
    elif im.mode not in ("RGB", "RGBA", "L"): #need to know what valid ones are
        return True, "Invalid color space"
    else:
        return False, ""

#parse command line arguments
if len(sys.argv) == 1:
   print("No file path given. Scanning current working directory.")
   startPath = os.getcwd()
else:
    startPath = sys.argv[1]


#set up output CSV headings
outputCSV = [["filename", "path", "size (MB)", "color space", "MIME type", "corrupt?",
              "corrupt reason"]]

#walk through directoy and scan images
for root, dirs, files in os.walk(startPath):
    for name in files:
        if name.endswith((".tif")): #better way to ID these?
        
            fullPath = root + "\\" + name
            if os.stat(fullPath).st_size == 0:
                outputCSV.append([name,
                                  fullPath,
                                  0,
                                  "Unknown",
                                  "Unknown",
                                  True,
                                  "Zero-length file"])
            else:
                try:
                    im = Image.open(fullPath)

                    corrupt, reason = isCorrupt(im,fullPath)

                    outputCSV.append([name,
                                      fullPath,
                                      os.stat(fullPath).st_size/1000000,
                                      im.mode,
                                      Image.MIME[im.format],
                                      corrupt,
                                      reason])
                    im.close()
                    
                except UnidentifiedImageError:
                    outputCSV.append([name,
                                      fullPath,
                                      os.stat(fullPath).st_size/1000000,
                                      "Unknown",
                                      "Unknown",
                                      True,
                                      "Unable to open file with Pillow"])
                

#construct output file
outputFilename = "bad_image_report_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
            
with open(outputFilename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(outputCSV)

print("Your output file is: " + str(os.getcwd()) + "\\" + outputFilename)


