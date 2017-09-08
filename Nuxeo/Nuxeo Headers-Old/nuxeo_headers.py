#This script assumes that the file is a Tab Separated Value file (tsv)
#It assumes that the columns.txt is in the same filepath as the entered filepath and the file is named columns.txt
#It also requires that pandas library is installed: ****pip install pandas****
#It also assumes that columns with numbers are set and not changed
#Written by Niqui O'Neill
import csv
import os
import re
import pandas as pd
filepath = input('Enter File Path: ') 
columns_txt = os.path.join(filepath, "columns.txt")
columns_list = []
with open(columns_txt, 'r') as columns_file:  ##Adds all headers in columns.txt to list
	for column in columns_file:
		if column != '\n':
			columns_list.append(column.strip("\n").strip(" "))

for file in os.listdir(filepath): 
	if file.endswith(".tsv"):  ## line 12-13 check files in filepath and checks to make sure they are tsv
		with open(os.path.join(filepath, file)) as tsv: #opens file
			tsvreader = csv.DictReader(tsv, delimiter="\t") #uses csv reader to read file
			headers = tsvreader.fieldnames #grabs first row
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
				tsv_headers.append(header) #add headers to list, replaces any numbers with %d to match against list				
			print("Missing fields in %s" % file)
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
			missing = []
			for column in columns_list: #columns.txt list
				if '%d' not in column: #checks for any column that does not have a number
					if column not in tsv_headers: #checks to see if header in columns.txt are in headers in the tsv file
						missing.append(column) #if header in columns.txt is not in tsv file, adds header to list
				if bool(re.search('Creator', column)): #finds creator fields in the required fields list
					for numb in set(list(creator_numb)):  #set(list()) removes repeat numbers
						if column%numb not in headers: #formats the column with the number, checks to see if in tsv file
							missing.append(column%numb) # if not there add to missing list
				if bool(re.search('Description ', column)): #finds description fields in the required fields list
					for numb in set(list(description_numb)):
						if column%numb not in headers: #formats the column with the number, checks to see if in tsv file
							missing.append(column%numb) # if not there add to missing list
				if bool(re.search('Name', column)) and bool(re.search('Subject', column)): #finds subject name fields in the required fields list
					for numb in set(list(subject_numb)):
						if column%numb not in headers: #formats the column with the number, checks to see if in tsv file
							missing.append(column%numb) # if not there add to missing list
				if bool(re.search('Place', column)): #finds place fields in the required fields list
					for numb in set(list(place_numb)):
						if column%numb not in headers: #formats the column with the number, checks to see if in tsv file
							missing.append(column%numb) # if not there add to missing list
				if bool(re.search('Topic', column)) and bool(re.search('Subject', column)): #finds subject topic fields in the required fields list
					for numb in set(list(sub_top_numb)):
						if column%numb not in headers: #formats the column with the number, checks to see if in tsv file
							missing.append(column%numb) # if not there add to missing list
				if bool(re.search('Form/Genre', column)): #finds form/genre fields in the required fields list
					for numb in set(list(form_numb)):
						if column%numb not in headers: #formats the column with the number, checks to see if in tsv file
							missing.append(column%numb) # if not there add to missing list
							
			header_list = headers #sets a header list to headers in tsv file (line 16)
			for miss in missing: #cycles through missing headers
				header_list.append(miss) #appends to list of headers in tsv file
			df = pd.read_csv(os.path.join(filepath, file), sep='\t') #uses pandas to read tsv file
			with_missing = df.reindex(columns=header_list) #reindexes columns to add missing headers
			with_missing.to_csv(os.path.join(filepath, file), sep='\t', index=False) #writes to tsv file
			if len(missing) > 0:
				print("Missing %s fields: %s have been added\n"%(len(missing),missing))
			else:
				print("****All Fields Present!*****\n")
			