#This script requires that the python library 'opencv' is installed
#This can be done with the following command: pip install opencv-python
#The program takes a folder of images and grabs screen captures
#The spacer variable spaces how often screens are saved. 
#The spacer%100 == 0 tells the program that if spacer/100 has no remainder to save the image. This means that every 100 frames get saved. 
#
#This script assumes there is a file folder holding videos of some kind. If these videos are of different types, this script will have to run for each type.
import os
import cv2

filepath = input('Enter File Path: ') 
input_type = input('Enter Video Type: ')
count = 0
for file in os.listdir(filepath):
	if file.endswith(".%s" % input_type):
		path = os.path.join(filepath, file)
		vidcap = cv2.VideoCapture(path)
		savedirpath = os.path.join(filepath, "thumbs")
		if not os.path.exists(savedirpath):
			os.makedirs(savedirpath)
		count = 1
		spacer = 0
		while vidcap.isOpened():
			success, image = vidcap.read()
			if success and count < 6:
				filename, ext = file.split(".")
				if spacer%100 == 0:
					filename = filename + "_thumb_" + str(count)
					cv2.imwrite(os.path.join(savedirpath, '%s.png') % filename, image)
					count += 1
				spacer += 1
			else:
				break
		print("Success for file: %s" % file)
		cv2.destroyAllWindows()
		vidcap.release()
