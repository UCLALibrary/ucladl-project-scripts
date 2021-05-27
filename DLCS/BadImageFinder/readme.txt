Python script to identify corrupt TIFF (.tif) image files.

First, install dependencies:
pip install -r requirements.txt

Then run from command line:
badimagefinder.py C:\path\to\directory

The script will iterate through all subfolders of the given directory looking for .tif files.
If no directory is given, the current working directory will be searched.
The output is a .csv file in the current working directory. 