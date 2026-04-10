import pandas as pd
import os
import re

# Step 1: Load the JSON File
# as the datacollection file creates json based on the current dat , generalising the file selection 
data_folder = 'data/'
json_files = [f for f in os.listdir(data_folder) if re.match(r'trends_\d{8}\.json', f)]

if not json_files:
    raise FileNotFoundError(f"No trends_YYYYMMDD.json file found in {data_folder}")

# Sort files by date (assuming the format trends_YYYYMMDD.json)
json_files.sort(key=lambda x: x.split('_')[1].split('.')[0], reverse=True)
json_file_path = os.path.join(data_folder, json_files[0])

df = pd.read_json(json_file_path)
print(f"Loaded {len(df)} stories from {json_file_path}\n")


rows_after_cleaning = len(df)

# 2:Cleaning the Data

# 2a: Duplicates — remove any rows with the same post_id
df.drop_duplicates(subset=['post_id'], inplace=True)
print(f"After removing duplicates: {len(df)}")
rows_after_cleaning = len(df)

# 2b: Missing values — drop rows where post_id, title, or score is missing
df.dropna(subset=['post_id', 'title', 'score'], inplace=True)
print(f"After removing nulls: {len(df)}")
rows_after_cleaning = len(df)

# 2c: Data types — make sure score and num_comments are integers
df['score'] = df['score'].astype(int)
df['num_comments'] = df['num_comments'].fillna(0).astype(int) # Fill NaNs before converting to int

# 2d: Low quality — remove stories where score is less than 5
df = df[df['score'] >= 5]
print(f"After removing low scores: {len(df)}")
rows_after_cleaning = len(df)

# 2e: Whitespace — strip extra spaces from the title column
df['title'] = df['title'].str.strip()

output_csv_path = 'data/trends_clean.csv'
df.to_csv(output_csv_path, index=False)

print(f"\nSaved {rows_after_cleaning} rows to {output_csv_path}\n")

# stories per category
print("Stories per category:")
print(df['category'].value_counts().sort_index().to_string())
