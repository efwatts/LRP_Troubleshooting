#!/usr/bin/env python3

import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description="Filter transcript-level count matrix by transcript metadata")
    parser.add_argument("-c", "--counts", required=True, help="Path to transcript-level counts matrix CSV/TSV file")
    parser.add_argument("-m", "--metadata", required=True, help="Path to transcript metadata TSV file")
    parser.add_argument("-o", "--output", required=True, help="Path to save filtered transcript counts matrix")

    args = parser.parse_args()

    # Load input files
    counts = pd.read_csv(args.counts, sep=None, engine="python")  # auto-detect comma or tab
    metadata = pd.read_csv(args.metadata, sep="\t")

    # Check columns
    if "pb" not in metadata.columns or "id" not in counts.columns:
        raise ValueError("Expected 'pb' column in metadata and 'id' column in counts matrix.")

    # Filter transcript IDs based on metadata
    valid_transcripts = metadata["pb"].unique()
    filtered_counts = counts[counts["id"].isin(valid_transcripts)]

    # Save output
    filtered_counts.to_csv(args.output, sep="\t", index=False)
    print(f"Filtered transcript counts matrix saved to: {args.output}")

if __name__ == "__main__":
    main()