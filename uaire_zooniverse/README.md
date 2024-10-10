# UCLA DLP Universidad del Aire transcripts
This is a repository of helpful scripts for working with transcripts from our Universidad del Aire zooniverse project


# preprocess_transcripts.py
This script pre processes zooniverse transcripts for manual review in two steps:
1. Filter out all non transcription related workflows
2. Extract filenames and transcriptions from json_objects, clean up filenames, split transcriptions into csvs by filename and add "y/n" column for manual review

# flatten_transcript.py

After reviewing transcriptions, this script takes a list of transcriptions of individual audio snippets and flattens into one .txt file. The script also produces a contributers report listing the contributers by total contributions and accepted contributions

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

- Clone this repository locally
- Move the csv file containing the zooniverse data into the uaire_zooniverse folder
- cd into ucladl-project-scripts/uaire_zooniverse/ and run the following commands

### Pre-process transcripts to prepare for manual review
Enter the following command into the command prompt followed by the name of the zooniverse csv file and the name of the transcription workflow
Note: path to csv is relative

```python
python3 preprocess_transcripts.py /path/to/csv/file.csv 'workflow_name'
```




### Flatten .csv file of transcriptions
Enter the following command into the command prompt followed by the name of the csv file
 ```python 
python3 flatten_transcript.py /path/to/csv/file/file.csv 
 ```

After running this command the script will generate a .txt file containing the full transcript in the current working directory and a csv containing thre contributers report


