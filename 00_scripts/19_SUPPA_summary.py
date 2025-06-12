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

    # Load PSI values
    psi_df = pd.read_csv(args.psivec, sep="\t", index_col=0)
    psi_df.columns = [
        "X504_Q157R_PSI", "A258_Q157R_PSI", "A309_Q157R_PSI",
        "V335_WT_PSI", "V334_WT_PSI", "A310_WT_PSI"
    ]
    psi_df["avg_PSI_Q157R"] = psi_df[["X504_Q157R_PSI", "A258_Q157R_PSI", "A309_Q157R_PSI"]].mean(axis=1, skipna=True)
    psi_df["avg_PSI_WT"] = psi_df[["V335_WT_PSI", "V334_WT_PSI", "A310_WT_PSI"]].mean(axis=1, skipna=True)

    # Parse event info
    psi_df = psi_df.reset_index().rename(columns={"index": "Event_id"})
    psi_df[["Index", "Event_type", "Coordinates"]] = psi_df["Event_id"].apply(
        lambda x: pd.Series(split_event_info(x))
    )

    # Load SQANTI and extract PB to Ensembl gene ID mapping
    sqanti_df = pd.read_csv(args.sqanti, sep="\t", usecols=["isoform", "associated_gene"])
    sqanti_df["Index"] = sqanti_df["isoform"].str.extract(r'^(PB\.\d+)')  # extract PB.XX

    # Drop duplicates so each PB.XX maps to a single gene
    sqanti_gene_map = sqanti_df.drop_duplicates("Index")[["Index", "associated_gene"]]

    # Merge using Index (PB.XX)
    psi_df = psi_df.merge(sqanti_gene_map, on="Index", how="left")

    # Load Ensembl-to-gene symbol map
    gene_map = pd.read_csv(args.gene_map, sep="\t", header=None, names=["associated_gene", "Gene"])
    psi_df = psi_df.merge(gene_map, on="associated_gene", how="left")

    # Load dPSI values and merge
    dpsi_df = pd.read_csv(args.dpsi, sep="\t")
    psi_df = psi_df.merge(dpsi_df, on="Event_id", how="left")
    psi_df = psi_df.rename(columns={
        "Q157R-WT_dPSI": "Q157R-WT_dPSI",
        "Q157R-WT_p-val": "Q157R-WT_p.value"
    })

    # Final output
    out_cols = [
        "Index", "Gene", "Event_type", "Coordinates",
        "V335_WT_PSI", "V334_WT_PSI", "A310_WT_PSI",
        "X504_Q157R_PSI", "A258_Q157R_PSI", "A309_Q157R_PSI",
        "avg_PSI_WT", "avg_PSI_Q157R", "Q157R-WT_dPSI", "Q157R-WT_p.value"
    ]
    psi_df[out_cols].to_csv(args.output, sep="\t", index=False)

if __name__ == "__main__":
    main()