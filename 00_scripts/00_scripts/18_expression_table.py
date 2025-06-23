#!/usr/bin/env python3

import pandas as pd
import argparse

def convert_fl_to_cpm(input_file, output_file):
    df = pd.read_csv(input_file, sep="\t")

    # Identify full-length count columns
    fl_cols = [col for col in df.columns if col.startswith("FL.")]
    if not fl_cols:
        raise ValueError("No columns starting with 'FL.' found")

    # Extract isoform column and FL counts
    isoforms = df["isoform"]
    fl_df = df[fl_cols].copy()
    sample_names = [col.replace("FL.", "") for col in fl_cols]

    # Calculate CPM
    lib_sizes = fl_df.sum(axis=0)
    cpm_df = fl_df.div(lib_sizes, axis=1) * 1e6

    # Combine isoforms with CPM values
    result_df = pd.concat([isoforms, cpm_df], axis=1)

    # Write header manually: sample names only (no 'transcript_id' header, no leading tab)
    with open(output_file, "w") as f:
        f.write("\t".join(sample_names) + "\n")
        result_df.to_csv(f, sep="\t", index=False, header=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert SQANTI FL counts to CPM for SUPPA2.")
    parser.add_argument("input_file", help="Path to SQANTI classification file")
    parser.add_argument("output_file", help="Path to output expression table for SUPPA2")
    args = parser.parse_args()
    convert_fl_to_cpm(args.input_file, args.output_file)