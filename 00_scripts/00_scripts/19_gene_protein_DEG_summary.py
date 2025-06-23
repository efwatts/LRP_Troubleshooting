#!/usr/bin/env python3

import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Compile gene summary table.")
    parser.add_argument("--cpm", required=True, help="Path to raw CPM matrix file")
    parser.add_argument("--deg", required=True, help="Path to gene DEG results")
    parser.add_argument("--class", dest="classification", required=True, help="Path to MDS classification file")
    parser.add_argument("--gene_map", required=True, help="Path to Ensembl-to-gene symbol mapping file")
    parser.add_argument("--output", required=True, help="Output summary file path")
    parser.add_argument("--wt_samples", nargs=3, required=True, help="Sample names for WT (in CPM header)")
    parser.add_argument("--q157r_samples", nargs=3, required=True, help="Sample names for Q157R (in CPM header)")
    parser.add_argument("--rename_samples", nargs='+', metavar='SAMPLE=RENAME', required=True,
                        help="Sample renaming map like BioSample_1=X504_Q157R")
    return parser.parse_args()

def parse_renames(rename_args):
    rename_dict = {}
    for item in rename_args:
        key, value = item.split("=")
        rename_dict[key.strip()] = value.strip()
    return rename_dict

def main():
    args = parse_args()
    rename_dict = parse_renames(args.rename_samples)

    # Load CPM and rename samples
    cpm_df = pd.read_csv(args.cpm, sep="\t", index_col=0)
    cpm_df = cpm_df.rename(columns=rename_dict)
    cpm_df.reset_index(inplace=True)
    cpm_df = cpm_df.rename(columns={"index": "Gene"})
    cpm_df["Gene"] = cpm_df["Gene"].astype(str)

    # Load classification table (for mapping PB gene to Ensembl gene)
    class_df = pd.read_csv(args.classification, sep="\t", usecols=["pb", "pr_gene"])
    class_df["PB_Gene_ID"] = class_df["pb"].str.extract(r"(PB\.\d+)")  # Extract PB.* from pb
    class_df = class_df.drop_duplicates(subset="PB_Gene_ID")  # One gene per PB gene ID
    class_df = class_df.rename(columns={"pr_gene": "Ensembl_ID"})

    # Load Ensembl → Gene Symbol mapping
    gene_map = pd.read_csv(args.gene_map, sep="\t", header=None, names=["Ensembl_ID", "Gene_Symbol"])

    # Merge class table with gene symbol
    gene_info = class_df.merge(gene_map, on="Ensembl_ID", how="left")

    # Merge CPM with gene info
    merged = cpm_df.merge(gene_info, left_on="Gene", right_on="PB_Gene_ID", how="left")

    # Calculate average CPMs
    merged["avg_CPM_WT"] = merged[args.wt_samples].mean(axis=1)
    merged["avg_CPM_Q157R"] = merged[args.q157r_samples].mean(axis=1)

    # Load DEG table
    deg_df = pd.read_csv(args.deg, sep="\t")
    deg_df.reset_index(inplace=True)
    deg_df = deg_df.rename(columns={"index": "Gene"})
    deg_df["Gene"] = deg_df["Gene"].astype(str)

    # Rename DEG columns
    deg_df = deg_df.rename(columns={
        "logFC": "logFC",
        "PValue": "p.value_DEG",
        "FDR": "FDR_DEG"
    })

    # Merge DEG
    merged = pd.merge(merged, deg_df, on="Gene", how="left")

    # Keep only genes with DEG result
    merged = merged[merged["logFC"].notna()]

    # Final column selection
    output_cols = [
        "Gene", "Gene_Symbol", "Ensembl_ID",
        *args.wt_samples, *args.q157r_samples,
        "avg_CPM_WT", "avg_CPM_Q157R", "logFC", "p.value_DEG", "FDR_DEG"
    ]
    output_cols_present = [col for col in output_cols if col in merged.columns]
    merged = merged[output_cols_present]
    merged = merged.rename(columns={"Gene": "Index", "Gene_Symbol": "Gene"})

    # Save output
    merged.to_csv(args.output, sep="\t", index=False)
    print(f"✅ Gene summary written to: {args.output}")

if __name__ == "__main__":
    main()