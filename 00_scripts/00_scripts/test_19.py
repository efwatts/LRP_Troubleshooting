import pandas as pd

# Load both files
summary = pd.read_csv("19_LRP_summary/protein_isoform_summary.tsv", sep="\t", dtype={"Isoform_index": str})
deg = pd.read_csv("19_LRP_summary/edgeR/transcript_DEG_results.txt", sep="\t", index_col=0)

# Print first 10 Isoform_index values
print("Isoform_index values from summary:")
print(summary["Isoform_index"].drop_duplicates().head(10))

# Print first 10 DEG index values
print("\nIndex values from transcript_DEG_results.txt:")
print(deg.index.to_series().head(10))