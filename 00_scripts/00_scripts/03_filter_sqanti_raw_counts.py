#!/usr/bin/env python3

import pandas as pd
import argparse

def simplify_fl_counts(input_file, output_file):
    # Load input
    df = pd.read_csv(input_file, sep='\t')
    
    # Define the columns you want to extract
    sample_cols = [
        "FL.BioSample_1", "FL.BioSample_2", "FL.BioSample_3",
        "FL.BioSample_4", "FL.BioSample_5", "FL.BioSample_6"
    ]
    
    # Subset and rename
    counts_df = df[["isoform"] + sample_cols].copy()
    counts_df = counts_df.rename(columns={
        "isoform": "id",
        "FL.BioSample_1": "BioSample_1",
        "FL.BioSample_2": "BioSample_2",
        "FL.BioSample_3": "BioSample_3",
        "FL.BioSample_4": "BioSample_4",
        "FL.BioSample_5": "BioSample_5",
        "FL.BioSample_6": "BioSample_6"
    })
    
    # Write to file
    counts_df.to_csv(output_file, sep=",", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simplify FL counts from SQANTI-style table")
    parser.add_argument("--input", required=True, help="Path to input TSV file")
    parser.add_argument("--output", required=True, help="Path to output CSV file")
    args = parser.parse_args()
    
    simplify_fl_counts(args.input, args.output)