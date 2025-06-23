#!/usr/bin/env python3

import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Filter and annotate condition-specific protein GTFs with CPM and gene info.")
    parser.add_argument("-i", "--input", required=True, help="Transcript summary table with CPM values")
    parser.add_argument("--gtf_q157r", required=True, help="Input GTF file for Q157R condition")
    parser.add_argument("--gtf_wt", required=True, help="Input GTF file for WT condition")
    parser.add_argument("-m", "--output_mutant", required=True, help="Output GTF file for Q157R")
    parser.add_argument("-w", "--output_wt", required=True, help="Output GTF file for WT")
    return parser.parse_args()

def load_isoform_map(summary_file):
    df = pd.read_csv(summary_file, sep="\t")

    isoform_map = {}
    for _, row in df.iterrows():
        pb_id = row["Transcript"]
        gene = row["Gene"]
        q157r_cpm = row["avg_CPM_Q157R"]
        wt_cpm = row["avg_CPM_WT"]
        isoform_map[pb_id] = {
            "gene": gene,
            "q157r_cpm": q157r_cpm,
            "wt_cpm": wt_cpm
        }
    return isoform_map

def filter_and_annotate_gtf(input_gtf, output_gtf, isoform_map, condition_key):
    count = 0
    with open(input_gtf) as fin, open(output_gtf, "w") as fout:
        for line in fin:
            if line.startswith("#") or line.strip() == "":
                continue
            parts = line.strip().split("\t")
            attr_field = parts[8]

            if 'transcript_id "' not in attr_field:
                continue

            # Extract PB accession from compound transcript_id
            try:
                tid_full = attr_field.split('transcript_id "')[1].split('"')[0]
                pb_id = tid_full.split("|")[1]  # Get PB.10.1 from Mrpl15|PB.10.1|pNNC|...
            except IndexError:
                continue

            if pb_id not in isoform_map:
                continue

            cpm = isoform_map[pb_id][condition_key]
            if cpm <= 0:
                continue

            gene = isoform_map[pb_id]["gene"]
            new_tid = f"{gene}|{pb_id}|{cpm:.6f}"

            parts[1] = "mm39_canon"
            parts[8] = f'gene_id "{gene}"; transcript_id "{new_tid}";'
            fout.write("\t".join(parts) + "\n")
            count += 1

    print(f"Wrote {count} transcripts to {output_gtf}")

def main():
    args = parse_args()
    isoform_map = load_isoform_map(args.input)

    filter_and_annotate_gtf(args.gtf_q157r, args.output_mutant, isoform_map, "q157r_cpm")
    filter_and_annotate_gtf(args.gtf_wt, args.output_wt, isoform_map, "wt_cpm")

if __name__ == "__main__":
    main()