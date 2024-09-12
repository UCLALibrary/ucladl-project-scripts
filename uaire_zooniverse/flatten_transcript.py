import pandas as pd, sys

filename = sys.argv[1]

df = pd.read_csv(filename)

df_total_contributions = df[["user_name", "classification_id"]].groupby("user_name").count().reset_index().rename(columns = {"classification_id":"total_contributions"})

df_accepted_contributions = df[["user_name", "y/n"]]
df_accepted_contributions = df_accepted_contributions[df_accepted_contributions["y/n"] == "Y"].groupby("user_name").count().reset_index().rename(columns = {"y/n":"accepted_contributions"})
final = pd.merge(df_accepted_contributions, df_total_contributions, on='user_name')
final.sort_values(by=['total_contributions'], ascending=False).to_csv(f"{filename[:-4]}_contributors_report.csv", index = False)

transcript = " ".join(df[df["y/n"] == "Y"]["transcriptions"])

with open(f"{filename[:-4]}_transcript.txt", "w") as text_file:
    text_file.write(transcript)

print(f"Contributers report saved as '{filename[:-4]}_contributors_report.csv'")
print(f"Transcript saved as '{filename[:-4]}_transcript.txt'")