# UCLA DLP Universidad del Aire transcripts
This is a repository of helpful scripts for working with transcripts from our Universidad del Aire zooniverse project

# Flatten transcripts

After review, this script takes a list of transcriptions of individual audio snippets and flattens into one .txt file

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

### Flatten .csv file of transcriptions
Enter the following command into the command prompt followed by the name of the csv file
 ```python 
python3 flatten_transcript.py /path/to/csv/file/file.csv 
 ```

 After running this command the script will generate a .txt file containing the full transcript in the current working directory