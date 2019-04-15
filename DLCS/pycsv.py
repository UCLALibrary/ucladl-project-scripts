import argparse
import csv
import functools
import io
import os
import pprint
import re


def clean(dirty):
    '''
    Returns a cleaned string, stripped of all newlines and carriage returns.
    '''
    return dirty.replace('\r', '').replace('\n', '')

metadata = {}
csvHeaders = ['Project Name','Item Ark', 'Parent Ark', 'Object Type', 'File Name']
nRows = 0


cursor = csv.DictReader(open("export.csv", encoding="utf-8"), 
    delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)


for row in cursor:

    # Identify the fields that we are interested in and put in variables
    # The keys will match the csv header 
    #project_title, item_ark, core_desc_term, qualifier_label, text_value, parent_ark, object_name, file_name
    
    project_title = row['PROJECT_TITLE']
    item_ark = row['ITEM_ARK'] 
    desc_term_label = row['CORE_DESC_TERM'] 
    qualifier_label = row['QUALIFIER_LABEL'] 
    text_value = row['TEXT_VALUE']
    parent_ark = row['PARENT_ARK']
    object_type = row['OBJECT_TYPE']
    file_name = row['FILE_NAME']

    nRows += 1
    # check if we've started accounting for this item yet
    if item_ark not in metadata:
        metadata[item_ark] = {
            'Project Name': project_title,
            'Item Ark': item_ark,
            'Parent Ark': parent_ark,
            'Object Type': object_type,
            'File Name': file_name,
            'Item Sequence': ''
        }
    #if qualifier_label is None or is "":
    if qualifier_label == False or len(qualifier_label) <= 0:
        inner_dict_key = desc_term_label
        
    else:
        inner_dict_key = '{0}.{1}'.format(desc_term_label, qualifier_label)

    # check if we've encountered a new header field
    if inner_dict_key not in csvHeaders:
        csvHeaders.append(inner_dict_key)

    # check if inner_dict_key already maps to a value
    if inner_dict_key in metadata[item_ark]:
        metadata[item_ark][inner_dict_key] = '{0}|~|{1}'.format(
            metadata[item_ark][inner_dict_key],
            text_value
        )
    else:
        metadata[item_ark][inner_dict_key] = text_value


if nRows == 0:
    print('Error: collection has no items!')

with open('tempcsv.csv', 'w', newline='', encoding='utf-8') as f:
    csvWriter = csv.writer(
        f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    # write header
    csvWriter.writerow([clean(i) for i in csvHeaders])

    # write a line for each item in the collection
    for k, v in sorted(metadata.items(), key=lambda x: x[0]):
        try:
            cleanedValuesList = [
                clean(v[i])
                # check csvHeaders to determine if value should be
                # included
                if i in v and v[i] is not None else ''
                for i in csvHeaders
            ]
        except AttributeError as e:
            print("error")
            raise
        csvWriter.writerow(cleanedValuesList)
