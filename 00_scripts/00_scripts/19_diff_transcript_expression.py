#!/usr/bin/env python3

import pandas as pd
import argparse

def compile_transcript_DE(edgeR_file, summary_file, output_file):
    # Load summary table
    summary_df = pd.read_csv(summary_file, sep="\t", dtype={"Isoform_index": str})
    print("Summary file loaded:", list(summary_df.columns))

    # Load edgeR results (transcripts as index, no transcript_id column)
    deg_df = pd.read_csv(edgeR_file, sep="\t", index_col=0)
    print("DEG file loaded. Index used as PB isoform ID.")

    # Create Isoform_index column for merging by stripping 'PB.' prefix
    deg_df["Isoform_index"] = deg_df.index.astype(str).str.replace("PB.", "", regex=False)

    # Rename columns for consistency
    deg_df.rename(columns={
        "logCPM": "avg_expr",
        "logFC": "delta",
        "PValue": "p.value"
    }, inplace=True)

    # Merge summary and DE results
    merged = pd.merge(summary_df, deg_df, on="Isoform_index", how="left")

    # Drop rows where DE info is missing
    merged = merged.dropna(subset=["avg_expr", "delta", "p.value"])

    # Select and reorder output columns
    output_df = merged[["Isoform_index", "Transcript", "Gene", "avg_expr", "delta", "p.value"]].copy()
    output_df.columns = ["Transcript_index", "Transcript", "Gene", "avg_expr", "delta", "p.value"]

    # Write to output
    output_df.to_csv(output_file, sep="\t", index=False)
    print(f"Wrote final output to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile edgeR results with a summary table for differential transcript expression analysis.")
    parser.add_argument("-e", "--edgeR", required=True, help="Path to edgeR results CSV file")
    parser.add_argument("-s", "--summary", required=True, help="Path to summary table TSV file")
    parser.add_argument("-o", "--output", required=True, help="Output file name for the final differential expression table")
    args = parser.parse_args()

    compile_transcript_DE(args.edgeR, args.summary, args.output)