import argparse
import csv
import os
import pandas as pd
from pathlib import Path
from pathlib import PureWindowsPath, PurePosixPath

def list_diff(l_1,l_2):
    '''returns list of items in first list, but not second'''
    return(list(set(l_1) - set(l_2)))

def get_merged_lists(csv_list, disk_list, path):
    csv_extras = list_diff(csv_list, disk_list)
    disk_extras = list_diff(disk_list, csv_list)
    out_dict_list = []
    for file in csv_list:
        if file in csv_extras:
            on_disk = False
            on_csv = True
        else:
            on_disk = True
            on_csv = True
        #format item name as it will be in spreadsheet
        file = os.path.relpath(file, path)
        file = str(PurePosixPath(PureWindowsPath(file)))
        out_dict_list.append({'File Name': file,
                              'On disk': on_disk,
                              'On CSV': on_csv})
    for file in disk_extras:
        on_disk = True
        on_csv = False
        #format item name as it will be in spreadsheet
        file = os.path.relpath(file, path)
        file = str(PurePosixPath(PureWindowsPath(file)))
        out_dict_list.append({'File Name': file,
                              'On disk': on_disk,
                              'On CSV': on_csv})
    return(out_dict_list)
    

def write_final_csv(csv, dict_list):
    csv_df = pd.read_csv(csv)
    #add columns for presence on disk and CSV, default to true
    csv_df['On disk'] = 'True'
    csv_df['On CSV'] = 'True'
    
    for item in dict_list:
        if item['On CSV'] == True and item['On disk'] == False:
            csv_df.loc[csv_df['File Name'] == item['File Name'], 'On disk'] = False
        elif item['On CSV'] == False and item['On disk'] == True:
            csv_df = csv_df.append(item, ignore_index = True)
    csv_df.to_csv(args.input_file, index=False)

#parse command line arguments
parser = argparse.ArgumentParser(description='Run audit of file inventory csv \
                                    vs. folder contents')
parser.add_argument('input_file',metavar='input', type=str, nargs = '?',
                    default = (r'C:\Zoe\ImageAudit\Test Materials\test_export.csv'),
                    help=r'filename of input csv to audit against, default = C:\Zoe\ImageAudit\Test Materials\test_export.csv')
parser.add_argument('filepath',metavar='path', type=str, nargs='?',
                    default = Path(r'C:\Zoe\ImageAudit\Test Materials\TestImages'),
                    help=r'path to files to audit, default = C:\Zoe\ImageAudit\Test Materials\TestImages')
args = parser.parse_args()

#read CSV file
csv_df_initial = pd.read_csv(args.input_file)
file_list_csv = []
raw_list_csv = csv_df_initial['File Name'].tolist()

for row in raw_list_csv:
    if not pd.isna(row):
        filename = Path(row)
        file_list_csv.append(os.path.join(args.filepath, filename))

#read directory contents
file_list_disk = []
for root, dirs, files in os.walk(args.filepath):
    for name in files:
        fullPath = os.path.join(root, name)
        file_list_disk.append(fullPath)

row_dicts = get_merged_lists(file_list_csv, file_list_disk, args.filepath)
write_final_csv(args.input_file, row_dicts)
