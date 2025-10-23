# ============================================
#  US Primary Election Vote Analysis (2016)
# ============================================

import pandas as pd
import matplotlib.pyplot as plt

# 1️⃣ Load the dataset correctly (semicolon separator)
df = pd.read_csv("US-2016-primary (1).csv", sep=';')

# 2️⃣ Check unique candidates
print(df['candidate'].unique())

# 3️⃣ Plot histogram for one candidate’s vote fraction
candidate_name = "Hillary Clinton"  # Change this to the exact name in your dataset
candidate_df = df[df['candidate'] == candidate_name]

plt.figure(figsize=(8,5))
plt.hist(candidate_df['fraction_votes'].dropna(), bins=20, edgecolor="black", color="skyblue")
plt.title(f"Distribution of Vote Fraction for {candidate_name}")
plt.xlabel("Vote Fraction")
plt.ylabel("Number of States (or Counties)")
plt.grid(axis='y', alpha=0.75)
plt.show()

# 4️⃣ Compare two candidates
candidate1 = "Hillary Clinton"
candidate2 = "Bernie Sanders"

df1 = df[df['candidate'] == candidate1].groupby('state')['fraction_votes'].mean()
df2 = df[df['candidate'] == candidate2].groupby('state')['fraction_votes'].mean()

combined = pd.DataFrame({
    candidate1: df1,
    candidate2: df2
}).dropna()

plt.figure(figsize=(8,6))
plt.scatter(combined[candidate1], combined[candidate2], color="purple", alpha=0.6)
plt.title(f"Vote Fraction Comparison: {candidate1} vs {candidate2}")
plt.xlabel(candidate1)
plt.ylabel(candidate2)
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()