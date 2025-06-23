#!/usr/bin/env python3

import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Summarize SUPPA splicing events with PSI, ΔPSI, and gene names.")
    parser.add_argument("--psivec", required=True, help="SUPPA PSI values file")
    parser.add_argument("--dpsi", required=True, help="SUPPA differential PSI file")
    parser.add_argument("--sqanti", required=True, help="SQANTI classification file with PB to Ensembl mapping")
    parser.add_argument("--gene_map", required=True, help="Ensembl-to-gene symbol table")
    parser.add_argument("--output", required=True, help="Output summary TSV file")
    parser.add_argument("--cond1_name", required=True, help="Human-readable name for Q157R (e.g. Q157R)")
    parser.add_argument("--cond2_name", required=True, help="Human-readable name for WT (e.g. WT)")
    return parser.parse_args()

def split_event_info(event_id):
    try:
        pbid, rest = event_id.split(';', 1)
        event_type, coords = rest.split(':', 1)
        return pbid, event_type, coords
    except:
        return event_id, "NA", "NA"

def main():
    args = parse_args()

    # Load PSI matrix
    psi_df = pd.read_csv(args.psivec, sep="\t", index_col=0)

    # Identify WT and Q157R sample columns
    cond1_cols = [c for c in psi_df.columns if c.startswith("Q157R")]
    cond2_cols = [c for c in psi_df.columns if c.startswith("WT")]

    # Rename for clarity
    rename_map = {}
    for i, col in enumerate(cond1_cols):
        rename_map[col] = f"{args.cond1_name}_{i+1}_PSI"
    for i, col in enumerate(cond2_cols):
        rename_map[col] = f"{args.cond2_name}_{i+1}_PSI"

    psi_df = psi_df.rename(columns=rename_map)

    # New column names
    cond1_renamed = list(rename_map[c] for c in cond1_cols)
    cond2_renamed = list(rename_map[c] for c in cond2_cols)

    # Compute averages
    psi_df[f"avg_PSI_{args.cond1_name}"] = psi_df[cond1_renamed].mean(axis=1, skipna=True)
    psi_df[f"avg_PSI_{args.cond2_name}"] = psi_df[cond2_renamed].mean(axis=1, skipna=True)

    # Reset index to extract event metadata
    psi_df = psi_df.reset_index().rename(columns={"index": "Event_id"})
    psi_df[["Index", "Event_type", "Coordinates"]] = psi_df["Event_id"].apply(
        lambda x: pd.Series(split_event_info(x))
    )

    # Map PB isoforms to Ensembl genes
    sqanti_df = pd.read_csv(args.sqanti, sep="\t", usecols=["isoform", "associated_gene"])
    sqanti_df["Index"] = sqanti_df["isoform"].str.extract(r'^(PB\.\d+)')
    sqanti_gene_map = sqanti_df.drop_duplicates("Index")[["Index", "associated_gene"]]

    # Add gene symbol
    gene_map = pd.read_csv(args.gene_map, sep="\t", header=None, names=["associated_gene", "Gene"])

    # Merge all gene info
    psi_df = psi_df.merge(sqanti_gene_map, on="Index", how="left")
    psi_df = psi_df.merge(gene_map, on="associated_gene", how="left")

    # Load ΔPSI table and merge
    dpsi_df = pd.read_csv(args.dpsi, sep="\t")
    psi_df = psi_df.merge(dpsi_df, on="Event_id", how="left")

    # Define output columns
    out_cols = ["Index", "Gene", "Event_type", "Coordinates"] + \
               cond1_renamed + cond2_renamed + \
               [f"avg_PSI_{args.cond1_name}", f"avg_PSI_{args.cond2_name}",
                f"{args.cond2_name}-{args.cond1_name}_dPSI", f"{args.cond2_name}-{args.cond1_name}_p-val"]

    # Write output
    psi_df[out_cols].to_csv(args.output, sep="\t", index=False)

if __name__ == "__main__":
    main()