# UCLA DLP Universidad del Aire transcripts
This is a repository of helpful scripts for working with transcripts from our Universidad del Aire zooniverse project

# Steps to process transcripts
1. First 

# preprocess_transcriptions.py
This script pre processes zooniverse transcripts for manual review in three steps:
- Extract workflows labelled "Transcribe audio (Spanish required)"
- 
- 

# flatten_transcript.py

After review transcriptions, this script takes a list of transcriptions of individual audio snippets and flattens into one .txt file. The script also produces a contributers report listing the contributers by total contributions and accepted contributions

## Set up

### Requirements
- python3.6
- pandas
- numpy

**Install dependencies (first-time setup only)**

```bash
pip3 install numpy pandas
```

## Usage

### Pre-process transcripts to prepare for manual review
Enter the following command into the command prompt followed by the name of the zooniverse csv file

### Flatten .csv file of transcriptions
Enter the following command into the command prompt followed by the name of the csv file
 ```python 
python3 flatten_transcript.py /path/to/csv/file/file.csv 
 ```

 After running this command the script will generate a .txt file containing the full transcript in the current working directory and a csv containing thre contributers report


