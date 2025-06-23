#!/usr/bin/env python3

import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Split SQANTI GTF by condition and update transcript/gene IDs.")
    parser.add_argument("-i", "--input", required=True, help="Input classification table (TSV)")
    parser.add_argument("-g", "--gtf", default="03_filter_sqanti/filtered.gtf", help="Input GTF file (default: filtered.gtf)")
    parser.add_argument("-p", "--pbmap", required=True, help="PB accession to gene symbol mapping table (TSV with columns: pb_acc, gene)")
    parser.add_argument("-m", "--output_mutant", required=True, help="Output GTF file for Q157R")
    parser.add_argument("-w", "--output_wt", required=True, help="Output GTF file for WT")
    return parser.parse_args()

def main():
    args = parse_args()

    q157r_cols = ["FL.BioSample_1", "FL.BioSample_2", "FL.BioSample_3"]
    wt_cols = ["FL.BioSample_4", "FL.BioSample_5", "FL.BioSample_6"]

    # === Load tables ===
    df = pd.read_csv(args.input, sep="\t")
    pb_map = pd.read_csv(args.pbmap, sep="\t").set_index("pb_acc")["gene"].to_dict()

    # === Convert FL counts to CPM ===
    for col in q157r_cols + wt_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Q157R_CPM"] = df[q157r_cols].sum(axis=1) / len(q157r_cols)
    df["WT_CPM"] = df[wt_cols].sum(axis=1) / len(wt_cols)

    # === Build isoform map with CPM and gene name ===
    isoform_map = {}
    for _, row in df.iterrows():
        isoform = row["isoform"]
        if isoform not in pb_map:
            continue  # skip if no gene name mapping
        gene_symbol = pb_map[isoform]
        isoform_map[isoform] = {
            "gene": gene_symbol,
            "q157r_cpm": row["Q157R_CPM"],
            "wt_cpm": row["WT_CPM"]
        }

    # === Write filtered and formatted GTF ===
    def write_gtf(filtered_isoforms, output_path):
        with open(args.gtf) as fin, open(output_path, "w") as fout:
            for line in fin:
                if line.startswith("#") or line.strip() == "":
                    continue
                parts = line.strip().split("\t")
                attr_field = parts[8]
                if 'transcript_id "' not in attr_field:
                    continue

                tid = attr_field.split('transcript_id "')[1].split('"')[0]
                if tid not in filtered_isoforms:
                    continue

                gene = isoform_map[tid]["gene"]
                cpm = filtered_isoforms[tid]
                new_tid = f"{gene}|{tid}|{cpm:.6f}"

                parts[1] = "mm39_canon"
                parts[8] = f'gene_id "{gene}"; transcript_id "{new_tid}";'
                fout.write("\t".join(parts) + "\n")

    q157r_isoforms = {k: v["q157r_cpm"] for k, v in isoform_map.items() if v["q157r_cpm"] > 0}
    wt_isoforms = {k: v["wt_cpm"] for k, v in isoform_map.items() if v["wt_cpm"] > 0}

    write_gtf(q157r_isoforms, args.output_mutant)
    write_gtf(wt_isoforms, args.output_wt)

    print(f"Wrote {len(q157r_isoforms)} Q157R transcripts to {args.output_mutant}")
    print(f"Wrote {len(wt_isoforms)} WT transcripts to {args.output_wt}")

if __name__ == "__main__":
    main()