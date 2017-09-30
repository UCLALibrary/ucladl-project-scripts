## ucla_google.py instructions
1. Go to https://console.developers.google.com/
2. Go to the Library tab
3. Search for "drive"
4. Click on the link for *Google Drive API*
5. Click on the *Enable* button
6. Click on *Create credentials*
7. Choose *service account key*
8. Fill out *Service account name, and service account ID*
9. Make sure Role is Project > Editor
10. Make sure key type is JSON
11. Rename the automatically downloaded file to *client_secret.json*
12. Open the *client_secret.json*
13. In the file find the *client_email* line, copy the email address
14. Share the folder holding the spreadsheets with the email address in the file
15. In the command line run
	
		pip install gspread oauth2client
16. run the script, make sure that the columns.txt file is in the same location as the script. 

**Note:** The script will run on any sheet shared with the email address

## nuxeo_headers.py instructions
For this script, make sure to use python3
1. Download Nuxeo Headers-Old folder
2. Install Pandas

		pip install pandas
		for mac - pip3 install pandas
3. Put spreadsheets in the same folder as the script and columns.txt file
4. run the script

		python nuxeo_headers.py
		for mac - python3 nuxeo_headers.py
5. Enter the filepath of the folder
6. Hit enter

