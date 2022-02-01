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
    
    alt_ID_cols = ['local ID', 'collection number']
    output_df['AltIdentifier.local'] = input_df[alt_ID_cols].apply(lambda row: ' | '.join(row.values.astype(str)), axis=1)

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
                'TypeOfResource':'Type.typeOfResource'}
    
    for key in map_dict.keys():
        if key in input_df.columns:
            output_df[map_dict[key]] = input_df[key].values
    return output_df


def map_constant_cols(output_df):
    output_df['Object Type'] = 'Work'
    output_df['viewingHint'] = 'individual'
    return output_df

def add_collection_record(input_df, output_df, cols):
    
    collection_row= pd.DataFrame({'Object Type':'Collection','Title':input_df['Digital Collection Title'][1]},
                    index = [0])

    output_df = pd.concat([collection_row,output_df]).reset_index(drop = True)
    return output_df
            


def main(input_file):
    input_df = pd.read_csv(input_file)

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

    output_df = map_concat_cols(input_df, output_df)
    output_df = map_constant_cols(output_df)
    output_df = map_simple_cols(input_df,output_df)
    output_df = add_collection_record(input_df, output_df, destination_cols)

    output_df.to_csv('MEAP_output.csv', index=False)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',metavar='input', type=str,
                        help=r'filename of input metadata csv')
    args = parser.parse_args(args)
    main(args.input_file)
