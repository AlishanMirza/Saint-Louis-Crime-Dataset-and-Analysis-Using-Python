# Simple St. Louis Crime Data Analysis
# Basic visualizations for assignment

import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np

folder = r"path\Dataset - CST\*.csv"
files = glob.glob(folder)

dfs = []
for file in files:
    df = pd.read_csv(file, low_memory=False, dtype={"IncidentNum": str})
    dfs.append(df)

crime = pd.concat(dfs, ignore_index=True)
print("Total records:", len(crime))

crime["IncidentDate"] = pd.to_datetime(crime["IncidentDate"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
crime = crime.dropna(subset=["IncidentDate"])

# Keep only data from 2023 onward (excludes 2022 and earlier)
crime = crime[crime["IncidentDate"].dt.year >= 2023]

# Plot 1: Monthly trends
monthly = crime.groupby(crime["IncidentDate"].dt.to_period("M")).size()
plt.figure(figsize=(12, 5))
plt.plot(monthly.index.astype(str), monthly.values, marker='o', linewidth=2)
plt.xticks(rotation=45)
plt.title("Monthly Crime Incidents")
plt.xlabel("Month")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig('monthly_crimes.png', dpi=150)
plt.close()

# Plot 2: Top 10 crimes
top_crimes = crime["NIBRSCategory"].value_counts().head(10)
plt.figure(figsize=(10, 6))
top_crimes.plot(kind='barh')
plt.title("Top 10 Crime Types")
plt.xlabel("Count")
plt.tight_layout()
plt.savefig('top_crimes.png', dpi=150)
plt.close()

print("Charts saved: monthly_crimes.png, top_crimes.png")