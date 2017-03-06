#this file requires the following to be installed: pandas
#this can be done on a machine with python by executing the following command:
#sudo pip install pandas

#this script takes in multiple spreadsheets and combines them into one spreadsheet
#it does this by having the user feed in a filepath of the spreadsheets, from there the script combines them.
#it also asks for the user to enter the name of the combined excel spreadsheet 
#This script is based upon a script found at the following url:
#http://stackoverflow.com/questions/15793349/how-to-concatenate-three-excels-files-xlsx-using-python


import pandas as pd
import glob
import os

try:
	filepath = raw_input("Enter File Path of Excel Spreadsheets:")
except:
	filepath = input("Enter File Path of Excel Spreadsheets:")
try:
	excel_file = raw_input("Enter file name without extension (will save to directory script is running from):")
except:
	excel_file = input("Enter file name without extension (will save to directory script is running from):")

# filenames

excel_names = []
excel = os.path.join(filepath, "*.xlsx")
for f in glob.glob(excel):
    excel_names.append(f)

# read files in
excels = [pd.ExcelFile(name) for name in excel_names]

# turn them into dataframes
frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]

# delete the first row (assumes that the headers are the first row)
frames[1:] = [df[1:] for df in frames[1:]]

# concatenate them..
combined = pd.concat(frames)

# write it out
filename = "{}.xlsx".format(excel_file)
combined.to_excel(filename, header=False, index=False)
