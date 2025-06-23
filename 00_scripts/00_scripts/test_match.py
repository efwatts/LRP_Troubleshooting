import pandas as pd

# Load your summary table
summary = pd.read_csv("19_LRP_summary/transcript_DEG_summary_table.tsv", sep="\t")

# Load DEG file (with PB accessions in the index)
deg = pd.read_csv("19_LRP_summary/edgeR/edgeR_transcript/top_transcripts.txt", sep="\t", index_col=0)

# Extract PB accessions
summary_ids = set(summary["Index"].astype(str))
deg_ids = set(deg.index.astype(str))

# Check which are missing
missing_ids = summary_ids - deg_ids

# Report
print(f"Total PB accessions in summary: {len(summary_ids)}")
print(f"Total PB accessions in DEG: {len(deg_ids)}")
print(f"PB accessions missing from DEG: {len(missing_ids)}")

# Optional: list the first few
if missing_ids:
    print("Example missing accessions:")
    print(list(missing_ids)[:10])