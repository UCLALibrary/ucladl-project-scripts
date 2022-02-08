import pandas as pd
import argparse
import csv
import os
from pathlib import Path
from pathlib import PureWindowsPath, PurePosixPath

def map_concat_cols(input_df, output_df):

    candidate_cols = ['Alt Title','English Translation of Title','Alternative Title']
    present_cols = []
    for col in candidate_cols:
        if col in input_df.columns:
            present_cols.append(col)
    output_df['AltTitle.other'] = input_df[present_cols].apply(lambda row: '|~|'.join(row.values.astype(str)), axis=1)

    candidate_cols = ['Abstract','Abstract | alb','Abtract | eng','Abstract | por']
    present_cols = []
    for col in candidate_cols:
        if col in input_df.columns:
            present_cols.append(col)
    output_df['Summary'] = input_df[present_cols].apply(lambda row: '|~|'.join(row.values.astype(str)), axis=1)
    
    candidate_cols =['local ID', 'collection number']
    present_cols = []
    for col in candidate_cols:
        if col in input_df.columns:
            present_cols.append(col)
    output_df['AltIdentifier.local'] = input_df[present_cols].apply(lambda row: ' | '.join(row.values.astype(str)), axis=1)

    output_df['File Name'] = 'Masters/othermasters/MEAPmigration/ramakatanearchive' + input_df['File name']

    
    return output_df


def map_simple_cols(input_df, output_df):
    map_dict = {'Subject.place':'Coverage.geographic',
                'Date.created':'Date.creation',
                'Date.created (single)':'Date.normalized',
                'Note.content':'Description.note',
                'Dimensions':'Format.dimensions',
                'Extent':'Format.extent',
                'Medium':'Format.medium',
                'Language | code':'Language',
                'Contributor.architect':'Name.architect',
                'Creator':'Name.creator',
                'Publisher.place':'Publisher.placeOfOrigin',
                'Publisher':'Publisher.publisherName',
                'collection name':'Relation.isPartOf',
                'Institution/Repository':'Repository',
                'Rights.copyrightStatus':'Rights.copyrightStatus',
                'Rights.servicesContact':'Rights.rightsHolderContact',
                'Subject.temporal':'Subject.temporal',
                'Subject':'Subject.conceptTopic',
                'Title':'Title',
                'Genre':'Type.genre',
                'TypeOfResource':'Type.typeOfResource',
                'Object Type':'Object Type'}
    
    for key in map_dict.keys():
        if key in input_df.columns:
            output_df[map_dict[key]] = input_df[key].values
    return output_df


def map_constant_cols(output_df):
    output_df['viewingHint'] = 'individual'
    return output_df

def add_coll_row(coll_df, works_df):
    full_df = pd.concat([coll_df,works_df]).reset_index(drop = True)
    return full_df

def preprocess_col_names(works_df):
    if ('Original language title' in works_df.columns) and (
        'Title' not in works_df.columns):
        works_df = works_df.rename(columns={'Original language title':'Title'})
    return works_df

def main(input_directory):

    for name in os.listdir(input_directory):
        if 'collection' in name:
            coll_file = name
        else:
            works_file = name

    coll_df = pd.read_csv(os.path.join(input_directory,coll_file))
    works_df = pd.read_csv(os.path.join(input_directory,works_file))
    works_df = preprocess_col_names(works_df)

    full_input_df = add_coll_row(coll_df, works_df)

    destination_cols=['Object Type','Title',
                      'Item ARK','Parent ARK',
                      'Rights.copyrightStatus','File Name',
                      'AltIdentifier.local','AltTitle.other',
                      'Coverage.geographic','Date.creation',
                      'Date.normalized','Description.latitude',
                      'Description.longitude','Description.note',
                      'Format.dimensions','Format.extent',
                      'Format.medium','Language',
                      'Name.architect','Name.repository',
                      'Publisher.publisherName','Relation.isPartOf',
                      'Rights.rightsHolderContact','Type.genre',
                      'Type.typeOfResource','Summary',
                      'viewingHint','Subject.conceptTopic',
                      'Subject temporal','Item Sequence',
                      'Name.creator', 'Publisher.placeOfOrigin']
    output_df = pd.DataFrame(columns=destination_cols)
    

    output_df = map_concat_cols(full_input_df, output_df)
    output_df = map_constant_cols(output_df)
    output_df = map_simple_cols(full_input_df,output_df)
    

    output_filename = 'MEAP_output_' + os.path.basename(input_directory) + '.csv'
    output_df.to_csv(output_filename, index=False)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_directory',metavar='input', type=str,
                        help=r'directory of input metadata csvs')
    args = parser.parse_args()
    main(args.input_directory)
