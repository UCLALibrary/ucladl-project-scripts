import pandas as pd
import numpy as np
import argparse
import csv
import sys
import os
from pathlib import Path
from pathlib import PureWindowsPath, PurePosixPath

def map_concat_cols(input_df, output_df, works_path):

    candidate_cols = ['English translation of title','Alternative Title','Translated Title']
    output_df = concat_helper(input_df, output_df, candidate_cols, 'AltTitle.other')
    
    candidate_cols =['Date.created (start)', 'Date.created (end)', 'Date.created (single)', 'Date.normalized']
    output_df = concat_helper(input_df, output_df, candidate_cols, 'Date.normalized')

    candidate_cols =['Repository', 'Institution/Repository']
    output_df = concat_helper(input_df, output_df, candidate_cols, 'Repository')

    candidate_cols =['Subject','Subject.topic']
    output_df = concat_helper(input_df, output_df, candidate_cols, 'Subject')

    candidate_cols =['Abstract','Summary','Description.note']
    output_df = concat_helper(input_df, output_df, candidate_cols, 'Description.note')

    candidate_cols =['Rights.servicesContact','Rights.rightsHolderContact']
    output_df = concat_helper(input_df, output_df, candidate_cols, 'Rights.rightsHolderContact')

    if works_path[-1] != '/':
        works_path = works_path + '/'
    output_df['File Name'] = works_path + input_df['File name']
    #hack for rajasthanmusic - replace mp3 with wav
    output_df['File Name'] = np.where(output_df['File Name'].str.contains('.mp3'), output_df['File Name'].str.slice(stop=-4)+'.wav',
                                    output_df['File Name'])
    
    return output_df

def concat_helper(input_df, output_df, candidate_cols, destination_col):
    present_cols = []
    for col in candidate_cols:
        if col in input_df.columns:
            present_cols.append(col)
    if len(present_cols) == 2:
        if 'Date.created (start)' in present_cols:
            output_df[destination_col] = input_df[present_cols[0]].astype(str).str.cat(input_df[present_cols[1]].astype(str),sep='/')
        else:
            output_df[destination_col] = input_df[present_cols[0]].astype(str).str.cat(input_df[present_cols[1]].astype(str))
    elif len(present_cols) == 1:
        output_df[destination_col] = input_df[present_cols[0]]
    elif len(present_cols) == 3:
        if 'Date.normalized' in present_cols:
            output_df[destination_col] = input_df['Date.normalized']
        elif 'Date.created (single)' in present_cols:
            output_df[destination_col] = input_df['Date.created (single)']
        else:
            output_df[destination_col] = input_df[present_cols[0]].astype(str).str.cat(input_df[present_cols[1:]],na_rep='')
    return output_df

def map_simple_cols(input_df, output_df):
    map_dict = {'Item ARK':'Item ARK',
                'Parent ARK':'Parent ARK',
                'Object Type':'Object Type',
                'collection name':'collection.physical',
                'Note.content':'Contents note',
                'Contributor':'Contributor',
                'Date.created':'Date.created',
                'Description.latitude':'Description.latitude',
                'Description.longitude':'Description.longitude',
                'Dimensions':'Format.dimensions',
                'Extent':'Format.extent',
                'Medium':'Format.medium',
                'Genre':'Genre',
                'Language | code':'Language',
                'local ID':'Local identifier',
                'Creator':'Name.creator',
                'Subject.name':'Named subject',
                'Note | eng':'Note',
                'Publisher.place':'Place of origin',
                'Publisher':'Publisher.publisherName',
                'TypeOfResource':'Resource type',
                'Rights.copyrightStatus':'Rights.copyrightStatus',
                'Note.statementofresponsibility':'Statement of Responsibility',
                'Subject.place':'Subject geographic',
                'Subject.temporal':'Subject temporal',
                'Title':'Title'}
    for key in map_dict.keys():
        if key in input_df.columns:
            output_df[map_dict[key]] = input_df[key].values
    return output_df


def map_constant_cols(output_df, is_complex, vh):
    if is_complex:
        output_df['viewingHint'] = vh
    return output_df

def add_coll_row(coll_df, works_df):
    full_df = pd.concat([coll_df,works_df]).reset_index(drop = True)
    return full_df

def map_mult_cols(input_df, output_df):
    dict1 = {'Institution/Repository':'Repository'}
    dict2 = {'Repository':'Repository'}
    for key in map_dict.keys():
            if key in input_df.columns:
                output_df[map_dict[key]] = input_df[key].values
    return output_df


def preprocess_col_names(works_df):
    if ('Original language title' in works_df.columns) and (
        'Title' not in works_df.columns):
        works_df = works_df.rename(columns={'Original language title':'Title'})
    return works_df

def add_item_pages(items_directory,works_df):
    destination_cols=['File Name','Object Type','Title',
                      'Item Sequence','Item ARK','Parent ARK']
    items_df = pd.DataFrame(columns=destination_cols)
    item_files = sorted(os.listdir(items_directory))
    filenames = works_df['File Name'][1:]
    print('Starting adding Page items. Total Work entries: ' + str(len(filenames)))
    tenpct = round(len(filenames)/10)
    #to keep track of pct progress
    i=0
    pct = 0 
    pct_count = 0
    for filename in filenames:
        name = os.path.split(filename)[1]
        file_ID = (name.split('.')[0])
        child_items = []

        for item in item_files:
            if file_ID in item:
                child_items.append(item)
        parent_ark = works_df.loc[works_df['File Name'] == filename,'Item ARK'].iloc[0]

        for child_item in child_items:
            digits=child_item.split('.')[0].split('_')[-1]
            if digits not in ['00','000','0000']:
                #fix file path
                filepath = str(PureWindowsPath(os.path.join(items_directory,child_item)).as_posix())
                while filepath[0] == '\\' or filepath[0] == '/':
                    filepath = filepath[1:]
                filepath = filepath.lower()
                filepath = filepath.capitalize()
                df=pd.DataFrame({'File Name':filepath,
                                 'Object Type':'Page',
                                 'Title':'Page '+digits.lstrip('0'),
                                 'Item Sequence':digits.lstrip('0'),
                                 'Parent ARK':parent_ark},index=[0])
                items_df = pd.concat([df,items_df],ignore_index=True)
        i=i+1
        if i > pct:
            print(str(pct_count) + '% done')
            pct = pct+tenpct
            pct_count = pct_count+10
    return items_df

def main():
    input_directory = input("Enter the directory containing metadata files: ").strip()
    works_directory = input("Enter the master images directory (e.g. Masters\othermasters...): ").strip()
    complex_items = input("Is this a complex (multiple pages per work) collection? Y/N: ")
	
    items_directory = ''
    viewing_hint = ''
    if complex_items == "Y" or complex_items == "y":
        items_directory = input("Enter the directory containing child item files: ")
        viewing_hint = input("Enter the viewing hint for all child items: ")
    
    #fix file path
    works_directory = str(PureWindowsPath(works_directory).as_posix())
    while works_directory[0] == '\\' or works_directory[0] == '/':
        works_directory = works_directory[1:]
    works_directory = works_directory.lower()
    works_directory = works_directory.capitalize()

    for name in os.listdir(input_directory):
        if 'collection' in name:
            coll_file = name
        else:
            works_file = name
    print('Reading Work and Collection metadata')
    coll_df = pd.read_csv(os.path.join(input_directory,coll_file))
    works_df = pd.read_csv(os.path.join(input_directory,works_file))
    works_df = preprocess_col_names(works_df)
    print('Adding Collection record to output')
    full_input_df = add_coll_row(coll_df, works_df)

    destination_cols=['Object Type','Title',
                      'Item ARK','Parent ARK','File Name',
                      'AltTitle.other','collection.physical',
                      'Contents note', 'Date.created',
                      'Date.normalized','Description.latitude',
                      'Description.longitude','Description.note',
                      'Format.dimensions','Format.extent',
                      'Format.medium','Genre',
                      'Language','Local identifier',
                      'Name.creator','Named subject',
                      'Note','Place of origin',
                      'Publisher.publisherName','Repository',
                      'Resource type', 'Rights.copyrightStatus',
                      'Rights.rightsHolderContact','Statement of Responsibility',
                      'Subject','Subject geographic',
                      'Subject temporal']
    output_df = pd.DataFrame(columns=destination_cols)

    print('Mapping work-level metadata')
    full_input_df = full_input_df.fillna('')
    output_df = map_concat_cols(full_input_df, output_df, works_directory)
    output_df = map_constant_cols(output_df,items_directory,viewing_hint)
    output_df = map_simple_cols(full_input_df,output_df)
    #remove path from collection row
    output_df['File Name'] = np.where(output_df['Object Type'] == 'Collection', '', output_df['File Name'])
    #if no object type was found, label as work
    output_df['Object Type'] = np.where(output_df['Object Type'] == '', 'Work', output_df['Object Type'])
    
    if items_directory:
        items_df = add_item_pages(items_directory,output_df)
        #remove file path from works df if complex
        output_df['File Name'] = ''
        print('Sorting Page entries')
        items_df = items_df.sort_values(['File Name','Item Sequence'],
                                        ascending=[True,True])
        items_filename = 'MEAP_output_' + os.path.basename(input_directory)+'_items' + '.csv'
        print('Outputting item-level results to ' + items_filename)
        items_df.to_csv(items_filename, index=False, na_rep='')

    output_filename = 'MEAP_output_' + os.path.basename(input_directory) + '.csv'
    print('Outputting work-level results to ' + output_filename)
    output_df.to_csv(output_filename, index=False, na_rep='')
    


if __name__ == '__main__':
    main()

