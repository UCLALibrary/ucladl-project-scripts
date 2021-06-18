import argparse
import csv
import os
import pandas as pd
print()
def list_diff(l_1,l_2):
    '''returns list of items in first list, but not second'''
    return(list(set(l_1) - set(l_2)))


#parse command line arguments
parser = argparse.ArgumentParser(description='Run audit of file inventory csv \
                                    vs. folder contents')
parser.add_argument('input_file',metavar='N', type=str,
                    help='filename of input csv to audit against')
parser.add_argument('filepath',metavar='N', type=str, nargs='?',
                    default = r'C:\Users\tucke\TestImages',
                    help='path to files to audit, default = DEFAULT')
args = parser.parse_args()

#read CSV file
csv_df = pd.read_csv(args.input_file)
file_list_csv = []
raw_list_csv = csv_df['File Name'].tolist()

for row in raw_list_csv:
    if not pd.isna(row):
        filename = row.replace('/', '\\')
        file_list_csv.append(args.filepath + '\\' + filename)

#read directory contents
file_list_disk = []
for root, dirs, files in os.walk(args.filepath):
    for name in files:
        fullPath = root + '\\'+  name
        file_list_disk.append(fullPath)

#add columns for presence on disk and CSV, default to true
csv_df['On disk'] = 'True'
csv_df['On CSV'] = 'True'

#Files on CSV, but not on disk
csv_extras = list_diff(file_list_csv, file_list_disk)
for item in csv_extras:
    item_name = item.replace(args.filepath, '')
    item_name_format = item_name.replace('\\', '/')[1:]
    csv_df.loc[csv_df['File Name'] == item_name_format, 'On disk'] = 'False'

#files on disk, but not csv
disk_extras = list_diff(file_list_disk, file_list_csv)

for item in disk_extras:
    item_name = item.replace(args.filepath, '')
    item_name_format = item_name.replace('\\', '/')[1:]
    row_dict = {'File Name': item_name_format,
                'On disk': 'True',
                'On CSV': 'False'}
    
    csv_df = csv_df.append(row_dict, ignore_index = True)

#write back to same CSV
csv_df.to_csv(args.input_file, index=False)
