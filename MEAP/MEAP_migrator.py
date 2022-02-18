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
                'Item ARK':'Item ARK',
                'Parent ARK':'Parent ARK',
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


def map_constant_cols(output_df, is_complex, vh):
    if is_complex:
        output_df['viewingHint'] = vh
    return output_df

def add_coll_row(coll_df, works_df):
    full_df = pd.concat([coll_df,works_df]).reset_index(drop = True)
    return full_df

def preprocess_col_names(works_df):
    if ('Original language title' in works_df.columns) and (
        'Title' not in works_df.columns):
        works_df = works_df.rename(columns={'Original language title':'Title'})
    return works_df

def add_item_pages(items_directory,works_df):
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
    items_df = pd.DataFrame(columns=destination_cols)
    item_files = sorted(os.listdir(items_directory))
    filenames = works_df['File Name'][1:]
    print('Starting adding Page items. Total Work files: ' + str(len(filenames)))
    tenpct = round(len(filenames)/10)
    i=0
    pct = 0
    pct_count = 0
    for filename in filenames:
        name = os.path.split(filename)[1]
        file_num = (name.split('.')[0]).split('_')[-1]
        child_items = []

        for item in item_files:
            if file_num in item:
                child_items.append(item)
        parent_ark = works_df.loc[works_df['File Name'] == filename,'Item ARK'].iloc[0]

        for child_item in child_items:
            digits=child_item.split('.')[0].split('_')[-1]
            if digits not in ['00','000','0000']:
                df=pd.DataFrame({'File Name':os.path.join(items_directory,child_item),
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

def main(input_directory, items_directory, viewing_hint):

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
    
    print('Mapping work-level metadata')
    output_df = map_concat_cols(full_input_df, output_df)
    output_df = map_constant_cols(output_df,items_directory,viewing_hint)
    output_df = map_simple_cols(full_input_df,output_df)
    
    if items_directory:
        items_df = add_item_pages(items_directory,output_df)
        print('Sorting Page entries')
        items_df = items_df.sort_values(['File Name','Item Sequence'],
                                        ascending=[True,True])
        items_filename = 'MEAP_output_' + os.path.basename(input_directory)+'_items' + '.csv'
        items_df.to_csv(items_filename, index=False, na_rep='')
    output_filename = 'MEAP_output_' + os.path.basename(input_directory) + '.csv'
    output_df.to_csv(output_filename, index=False, na_rep='')
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_directory',type=str,
                        help=r'directory of input metadata csvs')
    parser.add_argument('items_directory',type=str,
                        help = 'paginated material only - directory of child items')
    parser.add_argument('viewing_hint',type=str,
                        help = 'string to use as viewing hint for child items (complex only)')
    args = parser.parse_args()
    main(args.input_directory, args.items_directory, args.viewing_hint)

