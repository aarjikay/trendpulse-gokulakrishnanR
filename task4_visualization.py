import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data/trends_analysed.csv into a DataFrame
analysed_csv_path = 'data/trends_analysed.csv'
df_charts = pd.read_csv(analysed_csv_path)

# Create a folder called outputs/ if it doesn't exist
output_dir = 'outputs/'
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory '{output_dir}' ensured to exist.")

# Helper function to shorten titles
def shorten_title(title, max_length=50):
    if len(title) > max_length:
        return title[:max_length-3] + '...'
    return title

# Chart 1: Top 10 Stories by Score 
print("\nGenerating Chart 1: Top 10 Stories by Score...")

top_10_stories = df_charts.sort_values(by='score', ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x='score', y=top_10_stories['title'].apply(shorten_title), data=top_10_stories, hue='score', palette='viridis', legend=False)
plt.title('Top 10 Hacker News Stories by Score')
plt.xlabel('Score')
plt.ylabel('Story Title')
plt.tight_layout()
chart1_path = os.path.join(output_dir, 'chart1_top_stories.png')
plt.savefig(chart1_path)
plt.show()
print(f"Saved Chart 1 to {chart1_path}")

# --- Chart 2: Stories per Category ---

category_counts = df_charts['category'].value_counts().reset_index()
category_counts.columns = ['category', 'count']

plt.figure(figsize=(10, 6))
sns.barplot(x='category', y='count', data=category_counts, hue='category', palette='tab10', legend=False)
plt.title('Number of Stories per Category')
plt.xlabel('Category')
plt.ylabel('Number of Stories')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
chart2_path = os.path.join(output_dir, 'chart2_categories.png')
plt.savefig(chart2_path)
plt.show()
print(f"Saved Chart 2 to {chart2_path}")

# ---Chart 3: Score vs Comments ---
print("\nGenerating Chart 3: Score vs Comments...")

plt.figure(figsize=(10, 6))
sns.scatterplot(x='score', y='num_comments', hue='is_popular', data=df_charts, palette='coolwarm', s=100, alpha=0.7)
plt.title('Score vs. Number of Comments (Popularity Highlighted)')
plt.xlabel('Score')
plt.ylabel('Number of Comments')
plt.legend(title='Is Popular')
plt.tight_layout()
chart3_path = os.path.join(output_dir, 'chart3_scatter.png')
plt.savefig(chart3_path)
plt.show()
print(f"Saved Chart 3 to {chart3_path}")
