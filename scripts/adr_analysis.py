import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from itertools import combinations


sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)


df = pd.read_csv('C:\\Users\\Divya\\Documents\\GitHub\\Adverse-Drug-Reaction-Analysis\\data\\adr_dataset.csv')

print("=" * 90)
print("ADVERSE DRUG REACTION (ADR) ANALYSIS")
print("=" * 90)
print(f"Total chemicals/medicines analyzed: {len(df)}")
print(f"Total adverse reaction categories: {len(df.columns) - 1}")
print()

# all adverse reaction columns (all except the first column which is Chemical Compound)
adr_columns = df.columns[1:].tolist()

print("Adverse Reaction Categories:")
for i, category in enumerate(adr_columns, 1):
    print(f"  {i}. {category}")
print()

#  ANALYSIS 1: HIGH-RISK MEDICINES 
print("=" * 90)
print("ANALYSIS 1: HIGH-RISK MEDICINES")
print("=" * 90)

# how many adverse reactions each medicine causes
df['Total_ADRs'] = df[adr_columns].sum(axis=1)

# Sort by number of adverse reactions
high_risk_medicines = df.nlargest(15, 'Total_ADRs')[['Chemical Compound', 'Total_ADRs']]

print("\nTop 15 HIGH-RISK Medicines (causing most adverse reactions):")
for idx, (chem, count) in enumerate(zip(high_risk_medicines['Chemical Compound'], high_risk_medicines['Total_ADRs']), 1):
    percentage = (count / len(adr_columns)) * 100
    print(f"  {idx}. {chem[:50]}... : {int(count)} adverse reactions ({percentage:.1f}%)")
print()

#  ANALYSIS 2: SAFEST MEDICINES 
low_risk_medicines = df.nsmallest(10, 'Total_ADRs')[['Chemical Compound', 'Total_ADRs']]

print("=" * 90)
print("ANALYSIS 2: SAFEST MEDICINES")
print("=" * 90)
print("\nTop 10 SAFEST Medicines (causing fewest adverse reactions):")
for idx, (chem, count) in enumerate(zip(low_risk_medicines['Chemical Compound'], low_risk_medicines['Total_ADRs']), 1):
    percentage = (count / len(adr_columns)) * 100
    print(f"  {idx}. {chem[:50]}... : {int(count)} adverse reactions ({percentage:.1f}%)")
print()

#  ANALYSIS 3: MOST COMMON ADVERSE REACTIONS 
print("=" * 90)
print("ANALYSIS 3: MOST COMMON ADVERSE REACTIONS")
print("=" * 90)

#  how many medicines cause each adverse reaction
adr_frequency = df[adr_columns].sum(axis=0).sort_values(ascending=False)

print("\nMost frequently caused adverse reactions:")
for idx, (adr, count) in enumerate(adr_frequency.head(10).items(), 1):
    percentage = (count / len(df)) * 100
    print(f"  {idx}. {adr}: affects {int(count)} medicines ({percentage:.1f}%)")
print()

#  CHART 1: HIGH-RISK MEDICINES 
print("Creating Chart 1: Top 15 High-Risk Medicines...")
plt.figure(figsize=(12, 8))
top15 = df.nlargest(15, 'Total_ADRs')
chemical_names = [str(x)[:30] + '...' if len(str(x)) > 30 else str(x) for x in top15['Chemical Compound']]
plt.barh(range(len(top15)), top15['Total_ADRs'].values, color='crimson')
plt.yticks(range(len(top15)), chemical_names)
plt.xlabel('Number of Adverse Reactions')
plt.ylabel('Medicine/Chemical Compound')
plt.title('Top 15 High-Risk Medicines - Most Adverse Reactions')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('C:\\Users\\Divya\\Documents\\GitHub\\Adverse-Drug-Reaction-Analysis\\output\\1_high_risk_medicines.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 1_high_risk_medicines.png\n")

#  CHART 2: MOST COMMON ADVERSE REACTIONS 
print("Creating Chart 2: Most Common Adverse Reactions...")
plt.figure(figsize=(14, 8))
top_adrs = adr_frequency.head(15)
plt.barh(range(len(top_adrs)), top_adrs.values, color='steelblue')
plt.yticks(range(len(top_adrs)), [x[:40] + '...' if len(x) > 40 else x for x in top_adrs.index])
plt.xlabel('Number of Medicines Causing This Reaction')
plt.ylabel('Adverse Reaction Type')
plt.title('Top 15 Most Common Adverse Reactions')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('C:\\Users\\Divya\\Documents\\GitHub\\Adverse-Drug-Reaction-Analysis\\output\\2_common_adverse_reactions.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 2_common_adverse_reactions.png\n")

#  CHART 3: ADVERSE REACTIONS DISTRIBUTION 
print("Creating Chart 3: Adverse Reactions Distribution...")
plt.figure(figsize=(12, 6))
adr_dist = (df[adr_columns].sum(axis=0) / len(df)) * 100
top10_adrs = adr_dist.nlargest(10)
colors = plt.cm.viridis(np.linspace(0, 1, len(top10_adrs)))
plt.bar(range(len(top10_adrs)), top10_adrs.values, color=colors)
plt.xticks(range(len(top10_adrs)), [x[:25] + '...' if len(x) > 25 else x for x in top10_adrs.index], rotation=45, ha='right')
plt.ylabel('Percentage of Medicines (%)')
plt.xlabel('Adverse Reaction Type')
plt.title('Percentage of Medicines Causing Each Adverse Reaction')
plt.tight_layout()
plt.savefig('C:\\Users\\Divya\\Documents\\GitHub\\Adverse-Drug-Reaction-Analysis\\output\\3_adverse_reaction_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 3_adverse_reaction_distribution.png\n")

#  CHART 4: MEDICINE RISK LEVEL DISTRIBUTION 
print("Creating Chart 4: Medicine Risk Level Distribution...")
plt.figure(figsize=(10, 6))

# Categorize medicines by risk level
risk_levels = pd.cut(df['Total_ADRs'], bins=[0, 5, 10, 15, 20, 24], 
                     labels=['Very Low (0-5)', 'Low (6-10)', 'Medium (11-15)', 'High (16-20)', 'Very High (21+)'])
risk_counts = risk_levels.value_counts().sort_index()

colors_risk = ['green', 'yellow', 'orange', 'red', 'darkred']
plt.bar(range(len(risk_counts)), risk_counts.values, color=colors_risk)
plt.xticks(range(len(risk_counts)), risk_counts.index, rotation=45, ha='right')
plt.ylabel('Number of Medicines')
plt.xlabel('Risk Level')
plt.title('Distribution of Medicines by ADR Risk Level')
plt.tight_layout()
plt.savefig('C:\\Users\\Divya\\Documents\\GitHub\\Adverse-Drug-Reaction-Analysis\\output\\4_medicine_risk_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 4_medicine_risk_distribution.png\n")

#  CHART 5: HEATMAP OF TOP MEDICINES AND ADVERSE REACTIONS 
print("Creating Chart 5: ADR Heatmap (Top 20 Medicines)...")
top20_medicines = df.nlargest(20, 'Total_ADRs')
heatmap_data = top20_medicines[adr_columns].T

plt.figure(figsize=(14, 10))
sns.heatmap(heatmap_data, cmap='RdYlGn_r', cbar_kws={'label': 'Adverse Reaction (0=No, 1=Yes)'}, 
            xticklabels=[x[:20] + '...' if len(str(x)) > 20 else str(x) for x in top20_medicines['Chemical Compound']], 
            yticklabels=[x[:30] + '...' if len(x) > 30 else x for x in heatmap_data.index])
plt.title('ADR Heatmap: Top 20 High-Risk Medicines vs Adverse Reactions')
plt.xlabel('Medicine/Chemical Compound')
plt.ylabel('Adverse Reaction Type')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0, fontsize=8)
plt.tight_layout()
plt.savefig('C:\\Users\\Divya\\Documents\\GitHub\\Adverse-Drug-Reaction-Analysis\\output\\5_adr_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 5_adr_heatmap.png\n")

#  ANALYSIS 4: ADVERSE REACTION CORRELATION 
print("=" * 90)
print("ANALYSIS 4: ADVERSE REACTION PATTERNS")
print("=" * 90)

#  which adverse reactions often occur together
print("\nAdverse reactions often occurring together in high-risk medicines:")

top_adr_names = adr_frequency.head(5).index.tolist()
print(f"\nTop 5 most common adverse reactions:")
for i, adr in enumerate(top_adr_names, 1):
    count = int(adr_frequency[adr])
    print(f"  {i}. {adr}: {count} medicines")

print()

# ===== DETAILED REPORT =====
print("=" * 90)
print("SUMMARY REPORT")
print("=" * 90)

# Save detailed report to file
with open('C:\\Users\\Divya\\Documents\\GitHub\\Adverse-Drug-Reaction-Analysis\\output\\ADR_Report.txt', 'w') as f:
    f.write("ADVERSE DRUG REACTION (ADR) ANALYSIS REPORT\n")
    f.write("=" * 90 + "\n\n")
    
    f.write("DATASET OVERVIEW\n")
    f.write(f"Total medicines/chemicals analyzed: {len(df)}\n")
    f.write(f"Total adverse reaction categories: {len(adr_columns)}\n\n")
    
    f.write("TOP 15 HIGH-RISK MEDICINES:\n")
    f.write("-" * 90 + "\n")
    for idx, (chem, count) in enumerate(zip(high_risk_medicines['Chemical Compound'], high_risk_medicines['Total_ADRs']), 1):
        percentage = (count / len(adr_columns)) * 100
        f.write(f"{idx}. {chem}: {int(count)} adverse reactions ({percentage:.1f}%)\n")
    
    f.write("\n\nTOP 15 MOST COMMON ADVERSE REACTIONS:\n")
    f.write("-" * 90 + "\n")
    for idx, (adr, count) in enumerate(adr_frequency.head(15).items(), 1):
        percentage = (count / len(df)) * 100
        f.write(f"{idx}. {adr}: affects {int(count)} medicines ({percentage:.1f}%)\n")
    
    f.write("\n\nKEY FINDINGS:\n")
    f.write("-" * 90 + "\n")
    f.write(f"- Medicines causing 21+ adverse reactions: {len(df[df['Total_ADRs'] >= 21])}\n")
    f.write(f"- Medicines causing 11-20 adverse reactions: {len(df[(df['Total_ADRs'] >= 11) & (df['Total_ADRs'] < 21)])}\n")
    f.write(f"- Medicines causing 6-10 adverse reactions: {len(df[(df['Total_ADRs'] >= 6) & (df['Total_ADRs'] < 11)])}\n")
    f.write(f"- Medicines causing 0-5 adverse reactions: {len(df[df['Total_ADRs'] < 6])}\n")

print("✓ Report saved: ADR_Report.txt\n")

print("=" * 90)
print("✓ ALL ADR ANALYSES COMPLETED SUCCESSFULLY!")
print("=" * 90)
print("\nOutput files saved in: output/ folder")
print("1. high_risk_medicines.png")
print("2. common_adverse_reactions.png")
print("3. adverse_reaction_distribution.png")
print("4. medicine_risk_distribution.png")
print("5. adr_heatmap.png")
print("6. ADR_Report.txt")