import pandas as pd
import numpy as np
import os


cleaned_csv_path = 'data/trends_clean.csv'


# Load data/trends_clean.csv into a Pandas DataFrame
df_analysed = pd.read_csv(cleaned_csv_path)

# shape of the DataFrame
print(f"Loaded data: {df_analysed.shape}")

# Print the first 5 rows
print("\nFirst 5 rows:")
print(df_analysed.head().to_string())

# Calculate and print average score and average num_comments
average_score = df_analysed['score'].mean()
average_comments = df_analysed['num_comments'].mean()
print(f"\nAverage score   : {average_score:,.0f}")
print(f"Average comments: {average_comments:,.0f}")


#  the mean, median, and standard deviation of score
mean_score = np.mean(df_analysed['score'])
median_score = np.median(df_analysed['score'])
std_dev_score = np.std(df_analysed['score'])
print(f"Mean score   : {mean_score:,.0f}")
print(f"Median score : {median_score:,.0f}")
print(f"Std deviation: {std_dev_score:,.0f}")

# the highest score and lowest score
max_score = np.max(df_analysed['score'])
min_score = np.min(df_analysed['score'])
print(f"Max score    : {max_score:,.0f}")
print(f"Min score    : {min_score:,.0f}")

#  category with  the most stories
most_stories_category = df_analysed['category'].value_counts().idxmax()
most_stories_count = df_analysed['category'].value_counts().max()
print(f"\nMost stories in: {most_stories_category} ({most_stories_count} stories)")

# find story which has the most comments
most_commented_story = df_analysed.loc[df_analysed['num_comments'].idxmax()]
print(f"\nMost commented story: \"{most_commented_story['title']}\"  — {most_commented_story['num_comments']:,.0f} comments")


# Add 'engagement' column
df_analysed['engagement'] = df_analysed['num_comments'] / (df_analysed['score'] + 1)
# Add 'is_popular' column
df_analysed['is_popular'] = df_analysed['score'] > average_score
print("Added 'engagement' and 'is_popular' columns.")

# output path for the analyzed data
output_analysed_csv_path = 'data/trends_analysed.csv'

# Save the updated DataFrame 
df_analysed.to_csv(output_analysed_csv_path, index=False)
print(f"Saved updated DataFrame to {output_analysed_csv_path}")
