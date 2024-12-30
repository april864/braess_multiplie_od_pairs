import pandas as pd
import matplotlib.pyplot as plt
import adjustText

REF_FILE = "og.csv"
CAP_ADJ_FILE = "cap_adj.csv"
PROCESSED_FILE = 'cost_changes.csv'
IMG_FILE = 'cost_change_decrease_plot.png'

# Load the first CSV file into a DataFrame
df1 = pd.read_csv(CAP_ADJ_FILE)

# Load the second CSV file into a DataFrame
df2 = pd.read_csv(REF_FILE)

# Merge the two DataFrames on the 'OD pair' column
merged_df = pd.merge(df1, df2, on='OD pair', suffixes=('_edge_adjusted', '_original'))

# Compare the costs and determine whether the cost increases or decreases
merged_df['Cost Change'] = merged_df['Cost_edge_adjusted'] - merged_df['Cost_original']
merged_df['Change Type'] = merged_df['Cost Change'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')

# Load the resulting DataFrame to csv file
merged_df.to_csv(PROCESSED_FILE, index=False)

# Load the CSV file into a DataFrame
df = pd.read_csv(PROCESSED_FILE)

# Filter the DataFrame to include only rows where Change Type is 'Decrease'
df_decrease = df[df['Change Type'] == 'Decrease']

# Plotting
plt.figure(figsize=(14, 8))

# Scatter plot for OD pair against Cost Change
plt.scatter(df_decrease['OD pair'], df_decrease['Cost Change'], label='Cost Change', alpha=0.6)

# Adding labels and title
plt.xlabel('OD Pair')
plt.ylabel('Cost Change')
plt.title('OD Pairs with Decreased Cost (0.1x Capacity)')
plt.tight_layout()

# Label each point with its corresponding 'Edge adjusted'
texts = []
for i, row in df_decrease.iterrows():
    edge_adjusted_values = df_decrease[(df_decrease['OD pair'] == row['OD pair']) & 
                                       (df_decrease['Cost Change'] == row['Cost Change'])]['Edge adjusted'].unique()
    label = ', '.join(set(edge_adjusted_values))  # Join unique values with a comma
    print(row)
    print(label)

# Adjust text to avoid overlapping
adjustText.adjust_text(texts)

# Save the plot as a PNG file
plt.savefig(IMG_FILE, format='png')