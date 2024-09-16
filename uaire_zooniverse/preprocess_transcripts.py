import os, pandas as pd, json, re, sys


###################################
# Filter our transcription workflow
###################################

def extract_transcriptions(csv, workflow):
    transcriptions_only = csv[csv.workflow_name == workflow]
    return transcriptions_only  

################################################
# Extract filenames from subject_data column
################################################


# Clean filenames by properly formatting and adding leading 0 to file sequence
def clean_file_names(f):
    if re.search("_([0-9]{1}).mp3$", f):
        f = re.sub("([0-9]{1}).mp3$", f'000{re.search("([0-9]{1}).mp3$", f).group()}', f)
    elif re.search("_([0-9]{2}).mp3$", f):
        f = re.sub("([0-9]{2}).mp3$", f'00{re.search("([0-9]{2}).mp3$", f).group()}', f)
    elif re.search("_([0-9]{3}).mp3$", f):
       f = re.sub("([0-9]{3}).mp3$", f'0{re.search("([0-9]{3}).mp3$", f).group()}', f)
    return f



##########################################################
# Extract filenames from subject_data column json string
##########################################################

def get_file_name(s):
    s_object = json.loads(s)
    try:
        file_name = clean_file_names(s_object[next(iter(s_object))]["file_name"])
    except:
        file_name = clean_file_names(s_object[next(iter(s_object))]["filename"])
    return file_name

###############################################
# Get transcription from annotation json object
###############################################

def get_transcription(t):
    transcription = json.loads(t)[0]["value"]
    return transcription


##############################
# get unique base filenames
##############################

def extract_base_filename(s):
   return re.sub("(_[0-9]{4}).mp3$", '', s)
   

#############################################
# transform file passed using command line args
#############################################

filename = sys.argv[1]

df = extract_transcriptions(pd.read_csv(filename), "Transcribe audio (Spanish required)")
df["file_name"] = df["subject_data"].apply(get_file_name)
df["transcriptions"] = df["annotations"].apply(get_transcription)
unique_base_filenames = df["file_name"].apply(extract_base_filename).unique()


if not os.path.exists("individual-csvs"):
    os.makedirs("individual-csvs")


for i in unique_base_filenames:
    result = df[df["file_name"].str.contains(i)]
    result.to_csv(f'individual-csvs/{i}.csv', index=False)


