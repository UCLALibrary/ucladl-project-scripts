import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import os
import re
 
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

columns_list = []
with open('columns.txt', 'r') as columns_file:  ##Adds all headers in columns.txt to list
    for column in columns_file:
        if column != '\n':
            columns_list.append(column.strip("\n").strip(" ")) 

files = client.openall()
for file in files:
    sheet = client.open(file.title).sheet1

    list_of_hashes = sheet.get_all_records()

    headers = sheet.row_values(1)
    #headers = [x for x in headers if x != '']
    tsv_headers = [] 
    creator = []
    creator_numb = []
    description = []
    description_numb = []
    subject = []
    subject_numb = []
    place = []
    place_numb = []
    subject_topic = []
    sub_top_numb = []
    form = []
    form_numb = []
    date = []
    date_numb = []
    contributor = []
    contributor_numb = []
    language = []
    language_numb = []
    copyright = []
    copyright_numb = []
    place = []
    place_numb = []
    for header in headers: #cycles through headers in tsv file
        if bool(re.search(r'\d', header)) == True: #checks to see if there is a number in the header
            if bool(re.search('Creator', header)) == True: #checks to see if specific fields
                creator.append(header) #adds header to creator list
                numb = re.findall("\d+", header) #finds all numbers in creator header
                for num in numb: # for numbers in found numbers
                    creator_numb.append(int(num)) #append numbers to creators numbers list
            if bool(re.search('Description ', header)) == True:
                description.append(header)
                numb = re.findall("\d+", header)
                for num in numb:
                    description_numb.append(int(num))
            if bool(re.search('Name', header)) == True and bool(re.search('Subject', header)):
                subject.append(header)
                numb = re.findall("\d+", header)
                for num in numb:
                    subject_numb.append(int(num))
            if bool(re.search('Place', header)) == True:
                place.append(header)
                numb = re.findall("\d+", header)
                for num in numb:
                    place_numb.append(int(num))
            if bool(re.search('Topic', header)) == True and bool(re.search('Subject', header)):
                subject_topic.append(header)
                numb = re.findall("\d+", header)
                for num in numb:
                    sub_top_numb.append(int(num))
            if bool(re.search('Form/Genre', header)) == True:
                form.append(header)
                numb = re.findall("\d+", header)
                for num in numb:
                    form_numb.append(int(num))
            if bool(re.search('Date', header)) == True:
                date.append(header)
                numb = re.findall("\d+", header)
                for num in numb:
                    date_numb.append(int(num))
            if bool(re.search('Contributor', header)) == True:
                contributor.append(header)
                numb = re.findall("\d+", header)
                for num in numb:
                    contributor_numb.append(int(num))
            if bool(re.search('Language', header)) == True:
                language.append(header)
                numb = re.findall("\d+", header)
                for num in numb:
                    language_numb.append(int(num))
            if bool(re.search('Holder', header)) == True:
                copyright.append(header)
                numb = re.findall("\d+", header)
                for num in numb:
                    copyright_numb.append(int(num))
            if bool(re.search('Place', header)) == True:
                language.append(header)
                numb = re.findall("\d+", header)
                for num in numb:
                    place_numb.append(int(num))
        tsv_headers.append(re.sub('\d', '%d', header)) #add headers to list, replaces any numbers with %d to match against list             
    print("Missing fields in %s" % file.title)
    if len(creator_numb) < 1:
        creator_numb.append(1)
    if len(description_numb) < 1:
        description_numb.append(1)
    if len(subject_numb) < 1:
        subject_numb.append(1)
    if len(place_numb) < 1:
        place_numb.append(1)
    if len(sub_top_numb) < 1:
        sub_top_numb.append(1)
    if len(form_numb) < 1:
        form_numb.append(1)
    if len(date_numb) < 1:
        date_numb.append(1)
    if len(contributor_numb) < 1:
        contributor_numb.append(1)
    if len(language_numb) < 1:
        language_numb.append(1)
    if len(copyright_numb) < 1:
        copyright_numb.append(1)
    if len(place_numb) < 1:
        place_numb.append(1)
        
    missing = []
    for column in columns_list: #columns.txt list
        if '%d' not in column: #checks for any column that does not have a number
            if column not in tsv_headers: #checks to see if header in columns.txt are in headers in the tsv file
                missing.append(column) #if header in columns.txt is not in tsv file, adds header to list
        elif bool(re.search('Creator', column)): #finds creator fields in the required fields list
            for numb in set(list(creator_numb)):  #set(list()) removes repeat numbers
                if column%numb not in headers: #formats the column with the number, checks to see if in tsv file
                    missing.append(column%numb) # if not there add to missing list
        elif bool(re.search('Description ', column)): #finds description fields in the required fields list
            for numb in set(list(description_numb)):
                if column%numb not in headers: #formats the column with the number, checks to see if in tsv file
                    missing.append(column%numb) # if not there add to missing list
        elif bool(re.search('Name', column)) and bool(re.search('Subject', column)): #finds subject name fields in the required fields list
            for numb in set(list(subject_numb)):
                if column%numb not in headers: #formats the column with the number, checks to see if in tsv file
                    missing.append(column%numb) # if not there add to missing list
        elif bool(re.search('Place', column)): #finds place fields in the required fields list
            for numb in set(list(place_numb)):
                if column%numb not in headers: #formats the column with the number, checks to see if in tsv file
                    missing.append(column%numb) # if not there add to missing list
        elif bool(re.search('Topic', column)) and bool(re.search('Subject', column)): #finds subject topic fields in the required fields list
            for numb in set(list(sub_top_numb)):
                if column%numb not in headers: #formats the column with the number, checks to see if in tsv file
                    missing.append(column%numb) # if not there add to missing list
        elif bool(re.search('Form/Genre', column)): #finds form/genre fields in the required fields list
            for numb in set(list(form_numb)):
                if column%numb not in headers: #formats the column with the number, checks to see if in tsv file
                    missing.append(column%numb) # if not there add to missing list
        elif bool(re.search('Date %d', column)): 
            for numb in set(list(date_numb)):
                if column%numb not in headers: 
                    missing.append(column%numb) 
        elif bool(re.search('Contributor', column)): 
            for numb in set(list(contributor_numb)):
                if column%numb not in headers: 
                    missing.append(column%numb) 
        elif bool(re.search('Language', column)): 
            for numb in set(list(language_numb)):
                if column%numb not in headers: 
                    missing.append(column%numb) 
        elif bool(re.search('Holder', column)): 
            for numb in set(list(copyright_numb)):
                if column%numb not in headers: 
                    missing.append(column%numb)         
        elif bool(re.search('Place', column)): 
            for numb in set(list(place_numb)):
                if column%numb not in headers: 
                    missing.append(column%numb) 
        elif column not in tsv_headers:
            if "%d" in column:
                missing.append(column%1)    
            else:
                missing.append(column)      
                    
    header_list = headers #sets a header list to headers in tsv file (line 16)
    for miss in missing: #cycles through missing headers
        header_list.append(miss) #appends to list of headers in tsv file

    if len(missing) > 0:
        sheet.add_cols(len(missing))
        end = len(header_list)
        x = 1
        while x <= end:
            for header in header_list:
                sheet.update_cell(1, x, header)
                x += 1
        print("Missing %s fields: %s have been added\n"%(len(missing),missing))
    else:
        print("****All Fields Present!*****\n")
                
