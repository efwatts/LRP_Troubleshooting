#!/usr/bin/env python3

import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Generate gene-level DTU summary table with fractional abundance.")
    parser.add_argument("--deg_summary", required=True, help="Path to gene-level DEG summary TSV")
    parser.add_argument("--dtu", required=True, help="Path to DRIMSeq gene-level DTU results TSV")
    parser.add_argument("--output", required=True, help="Output path for gene DTU summary table")
    return parser.parse_args()

def main():
    args = parse_args()

    # Load DEG summary
    deg_df = pd.read_csv(args.deg_summary, sep="\t")

    # Define WT and Q157R samples
    wt_samples = ["V335_WT_CPM", "V334_WT_CPM", "A310_WT_CPM"]
    q157r_samples = ["X504_Q157R_CPM", "A258_Q157R_CPM", "A309_Q157R_CPM"]

    # Total CPM per sample group (denominator for frac calc)
    frac_df = deg_df.copy()
    frac_df["total_CPM_WT"] = frac_df[wt_samples].sum(axis=1)
    frac_df["total_CPM_Q157R"] = frac_df[q157r_samples].sum(axis=1)

    # Compute fractional abundance for each sample
    for col in wt_samples:
        new_col = col.replace("_CPM", "_Frac")
        frac_df[new_col] = frac_df[col] / frac_df["total_CPM_WT"]
    for col in q157r_samples:
        new_col = col.replace("_CPM", "_Frac")
        frac_df[new_col] = frac_df[col] / frac_df["total_CPM_Q157R"]

    # Compute average and delta frac
    frac_df["avg_Frac_WT"] = frac_df[[col.replace("_CPM", "_Frac") for col in wt_samples]].mean(axis=1)
    frac_df["avg_Frac_Q157R"] = frac_df[[col.replace("_CPM", "_Frac") for col in q157r_samples]].mean(axis=1)
    frac_df["delta_frac"] = frac_df["avg_Frac_Q157R"] - frac_df["avg_Frac_WT"]

    # Load DRIMSeq gene-level DTU results
    dtu_df = pd.read_csv(args.dtu, sep="\t")

    # Merge on Ensembl_ID = gene_id
    merged = frac_df.merge(dtu_df, how="left", left_on="Ensembl_ID", right_on="gene_id")

    # Rename DTU columns
    merged = merged.rename(columns={
        "lr": "lf_DTU",
        "pvalue": "p.value_DTU",
        "adj_pvalue": "adj_p.value_DTU"
    })

    # Final output columns
    out_cols = [
        "Index", "Gene", "Ensembl_ID",
        "V335_WT_Frac", "V334_WT_Frac", "A310_WT_Frac",
        "X504_Q157R_Frac", "A258_Q157R_Frac", "A309_Q157R_Frac",
        "avg_Frac_WT", "avg_Frac_Q157R", "delta_frac",
        "lf_DTU", "p.value_DTU", "adj_p.value_DTU"
    ]
    
    # Write to output
    merged[out_cols].to_csv(args.output, sep="\t", index=False)

if __name__ == "__main__":
    main()