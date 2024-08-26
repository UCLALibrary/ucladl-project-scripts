import pandas as pd, sys

filename = sys.argv[1]

df = pd.read_csv(filename)

transcript = " ".join(df[df["y/n"] == "Y"]["transcriptions"])

with open(f"{filename[:-4]}_transcript.txt", "w") as text_file:
    text_file.write(transcript)

print(f"Transcript saved as '{filename[:-4]}_transcript.txt'")