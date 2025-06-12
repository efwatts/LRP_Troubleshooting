#!/usr/bin/env python3

import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Generate transcript-level DTU summary table with fractional abundance.")
    parser.add_argument("--deg_summary", required=True, help="Path to transcript_DEG_summary.tsv")
    parser.add_argument("--dtu", required=True, help="Path to DRIMSeq DTU results (e.g., gene_id, feature_id, pvalue, adj_pvalue)")
    parser.add_argument("--output", required=True, help="Path to write the output summary table")
    return parser.parse_args()

def main():
    args = parse_args()

    # Load transcript DEG summary (includes CPM columns)
    deg_df = pd.read_csv(args.deg_summary, sep="\t")

    # Define sample columns
    wt_samples = ["V335_WT_CPM", "V334_WT_CPM", "A310_WT_CPM"]
    q157r_samples = ["X504_Q157R_CPM", "A258_Q157R_CPM", "A309_Q157R_CPM"]
    all_samples = wt_samples + q157r_samples

    # Create a copy for fractional abundance calculations
    frac_df = deg_df.copy()

    # Calculate fractional abundance per sample per gene
    for sample in all_samples:
        frac_col = sample.replace("_CPM", "_Frac")
        # Compute gene-level total CPM per sample
        gene_total = frac_df.groupby("Gene")[sample].transform("sum")
        # Compute transcript-level fractional abundance
        frac_df[frac_col] = frac_df[sample] / gene_total

    # Calculate average fractional abundance across replicates
    frac_df["avg_Frac_WT"] = frac_df[[col.replace("_CPM", "_Frac") for col in wt_samples]].mean(axis=1)
    frac_df["avg_Frac_Q157R"] = frac_df[[col.replace("_CPM", "_Frac") for col in q157r_samples]].mean(axis=1)

    # Load DRIMSeq DTU results
    dtu_df = pd.read_csv(args.dtu, sep="\t")

    # Merge DTU results into DEG summary using transcript ID
    merged_df = frac_df.merge(dtu_df, how="left", left_on="Index", right_on="feature_id")

    # Rename DTU result columns for clarity
    merged_df = merged_df.rename(columns={
        "lr": "lf_DTU",
        "pvalue": "p.value_DTU",
        "adj_pvalue": "adj.p.value_DTU"
    })

    # Select final output columns
    final_cols = [
        "Index", "Gene", "Transcript", "Classification", "Known/Novel",
        "V335_WT_Frac", "V334_WT_Frac", "A310_WT_Frac",
        "X504_Q157R_Frac", "A258_Q157R_Frac", "A309_Q157R_Frac",
        "avg_Frac_WT", "avg_Frac_Q157R",
        "lf_DTU", "p.value_DTU", "adj.p.value_DTU"
    ]

    # Write the output
    merged_df[final_cols].to_csv(args.output, sep="\t", index=False)

if __name__ == "__main__":
    main()