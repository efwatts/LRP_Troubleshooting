#!/usr/bin/env python3

import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description="Filter gene-level count matrix by transcript metadata")
    parser.add_argument("-c", "--counts", required=True, help="Path to counts matrix TSV file")
    parser.add_argument("-m", "--metadata", required=True, help="Path to transcript metadata TSV file")
    parser.add_argument("-o", "--output", required=True, help="Path to save filtered counts matrix")

    args = parser.parse_args()

    # Load files
    counts = pd.read_csv(args.counts, sep="\t")
    metadata = pd.read_csv(args.metadata, sep="\t")

    # Extract gene IDs from transcript IDs (e.g., PB.10.2 → PB.10)
    metadata["gene_id"] = metadata["pb"].apply(lambda x: ".".join(x.split(".")[:2]))

    # Get unique gene_ids
    valid_genes = metadata["gene_id"].unique()

    # Filter counts
    filtered_counts = counts[counts["gene_id"].isin(valid_genes)]

    # Save output
    filtered_counts.to_csv(args.output, sep="\t", index=False)
    print(f"Filtered counts matrix saved to: {args.output}")

if __name__ == "__main__":
    main()