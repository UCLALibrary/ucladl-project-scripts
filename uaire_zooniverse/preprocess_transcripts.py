import os, pandas as pd, json, re




###################################
# Filter our transcription workflow
###################################

def extract_transcriptions(csv, workflow):
    df = pd.read_csv(csv)
    transcriptions_only = df[df.workflow_name == workflow]
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

# Extract filenames from subject_data column json string
def get_file_name(s):
    s_object = json.loads(s)
    try:
        file_name = clean_file_names(s_object[next(iter(s_object))]["file_name"])
    except:
        file_name = clean_file_names(s_object[next(iter(s_object))]["filename"])
    return file_name


def extract_file_names(df):
    df["file_name"] = df["subject_data"].apply(get_file_name)


# move to top of dataframe
transcriptions_only = transcriptions_only[ ['file_name'] + [ col for col in transcriptions_only.columns if col != 'file_name' ] ]
#names = transcriptions_only['file_names']
#transcriptions_only.drop(labels=['file_names'], axis=1,inplace = True)
#transcriptions_only.insert(0, 'file_names', names)

#sort

transcriptions_only = transcriptions_only.sort_values("file_name")

transcriptions_only.to_csv("vintage-cuban-radio-classifications-trancriptions_part-1.csv", index=False)

def get_transcription(t):
    transcription = json.loads(t)[0]["value"]
    return transcription

transcriptions_only["transcriptions"] = transcriptions_only["annotations"].apply(get_transcription)
transcriptions = transcriptions_only['transcriptions']
transcriptions_only.drop(labels=['transcriptions'], axis=1,inplace = True)
transcriptions_only.insert(1, 'transcriptions', transcriptions)

transcriptions_only.to_csv("vintage-cuban-radio-classifications-trancriptions_part-2.csv", index=False)

##############################
# Split CSVs for manual review
##############################

transcriptions_only = pd.read_csv("vintage-cuban-radio-transcriptions-sorted.csv")

# get unique base filenames
def extract_base_filename(s):
    return re.sub("(_[0-9]{4}).mp3$", '', s)
    

unique_base_filenames = transcriptions_only["file_name"].apply(extract_base_filename).unique()


for i in unique_base_filenames:
    result = transcriptions_only[transcriptions_only["file_name"].str.contains(i)]
    result.to_csv(f'individual-csvs/{i}.csv', index=False)
