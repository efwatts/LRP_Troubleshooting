#!/usr/bin/env python3

import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Compile transcript summary table.")
    parser.add_argument("--cpm", required=True, help="Path to raw CPM matrix file")
    parser.add_argument("--deg", required=True, help="Path to transcript DEG results")
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
    cpm_df = cpm_df.rename(columns={"index": "Transcript"})
    cpm_df["Transcript"] = cpm_df["Transcript"].astype(str)

    # Load classification table
    cls_df = pd.read_csv(args.classification, sep="\t", usecols=[
        "isoform", "associated_gene", "associated_transcript", "structural_category"
    ])
    cls_df = cls_df.rename(columns={
        "isoform": "Transcript",
        "associated_gene": "Gene_ID",
        "associated_transcript": "Transcript_Ref",
        "structural_category": "Classification"
    })
    cls_df["Transcript"] = cls_df["Transcript"].astype(str)
    cls_df["Known/Novel"] = cls_df["Classification"].apply(lambda x: "K" if "match" in x else "N")

    # Load gene symbol map
    gene_map = pd.read_csv(args.gene_map, sep="\t", header=None, names=["Gene_ID", "Gene_Symbol"])
    cls_df = cls_df.merge(gene_map, how="left", on="Gene_ID")

    # Merge CPM with classification
    summary = pd.merge(cpm_df, cls_df, how="left", on="Transcript")
    summary["Transcript_Used"] = summary["Transcript_Ref"].where(summary["Transcript_Ref"] != "novel", summary["Transcript"])

    # Calculate average CPMs
    summary["avg_CPM_WT"] = summary[args.wt_samples].mean(axis=1)
    summary["avg_CPM_Q157R"] = summary[args.q157r_samples].mean(axis=1)

    # Load DEG and coerce first column to Transcript
    deg_df = pd.read_csv(args.deg, sep="\t", index_col=0).reset_index()
    deg_df = deg_df.rename(columns={"index": "Transcript"})
    deg_df["Transcript"] = deg_df["Transcript"].astype(str)

    # Rename DEG columns
    deg_rename_map = {}
    if "logFC" in deg_df.columns:
        deg_rename_map["logFC"] = "logFC_DEG"
    if "PValue" in deg_df.columns:
        deg_rename_map["PValue"] = "p.value_DEG"
    if "FDR" in deg_df.columns:
        deg_rename_map["FDR"] = "FDR_DEG"
    deg_df = deg_df.rename(columns=deg_rename_map)

    # Merge DEG results into summary
    summary = pd.merge(summary, deg_df, how="left", on="Transcript")

    # Filter: only transcripts that appear in both DEG and classification
    keep = summary["logFC_DEG"].notna() & summary["Classification"].notna()
    summary = summary[keep]

    # Diagnostics
    print("Columns after filtering:", summary.columns.tolist())
    print(f"Transcripts retained after filtering: {summary.shape[0]}")

    # Final column selection
    output_cols = [
        "Transcript", "Gene_Symbol", "Transcript_Used", "Classification", "Known/Novel",
        *args.wt_samples, *args.q157r_samples,
        "avg_CPM_WT", "avg_CPM_Q157R", "logFC_DEG", "p.value_DEG", "FDR_DEG"
    ]
    output_cols_present = [col for col in output_cols if col in summary.columns]

    summary_final = summary[output_cols_present].rename(columns={
        "Transcript": "Index",
        "Transcript_Used": "Transcript",
        "Gene_Symbol": "Gene"
    })

    summary_final.to_csv(args.output, sep="\t", index=False)
    print(f"\n✅ Summary written to: {args.output}")

if __name__ == "__main__":
    main()