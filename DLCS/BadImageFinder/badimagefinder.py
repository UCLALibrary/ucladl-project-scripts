import sys
import os
from PIL import Image
from PIL import UnidentifiedImageError
import csv
from datetime import datetime

#helper function to try the most common corruption tests
def isCorrupt(path):
    size = getFileSizeMB(path)
    if size == 0:
        return True, "Zero file size", None
    try:
        img = Image.open(path)
        if img.verify() is not None:
            return True, "Pillow verification failed", img
        elif img.filename[-3:] == "tif" and Image.MIME[img.format] != "image/tiff":
            return True, "Non-TIFF MIME type for .tif file", img
        elif img.mode not in ("RGB", "RGBA", "L"): #need to know what valid ones are
            return True, "Invalid color space", img
        else:
            return False, "", img
    except UnidentifiedImageError:
        return False, "Unable to open file with Pillow", None

def getFileSizeMB(filePath):
    size = os.stat(filePath).st_size
    if size != 0:
        size = size/1000000
    return size

def getModeAndMime(img, corrupt):
    if corrupt:
        return None, None
    else:
        mode = img.mode
        mime = Image.MIME[img.format]
        return mode, mime
    
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
        
            fullPath =  os.path.join(root, name)
                    
            corrupt, reason, im = isCorrupt(fullPath)

            mode, mime = getModeAndMime(im, corrupt)

            size = getFileSizeMB(fullPath)

            outputCSV.append([name,
                              fullPath,
                              size,
                              mode,
                              mime,
                              corrupt,
                              reason])

            if im is not None:
                im.close()


#construct output file
outputFilename = "bad_image_report_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
            
with open(outputFilename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(outputCSV)

print("Your output file is: " + str(os.getcwd()) + "\\" + outputFilename)


