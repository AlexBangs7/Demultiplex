#!/usr/bin/env python

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Generate dataframe from counts.txt

df = pd.read_csv('/scratch/bgmp/abangs/demux/counts.txt', sep='\t')
df[["Index1","Index2"]] = df["Barcode"].str.split('-', n=1, expand=True)

# Convert dataframe to array, with Indexes as row and column labels

pt = df.pivot_table(index='Index1',columns='Index2',values='Count',fill_value=0)
print(pt)
# Plot arrays on heatmaps

plt.figure(figsize=(8, 6))
sns.heatmap(pt, cmap = "viridis")
plt.title("Heatmap of sequenced index pairs (linear)")
plt.tight_layout()
plt.savefig("./outputs/heatmap")

plt.figure(figsize=(8, 6))
sns.heatmap(pt, norm=matplotlib.colors.LogNorm(), cmap = "viridis")
plt.title("Heatmap of sequenced index pairs (log10 scale)")
plt.tight_layout()
plt.savefig("./outputs/heatmap_logscale")