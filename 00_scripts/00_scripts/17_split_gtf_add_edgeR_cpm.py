#!/usr/bin/env python3

import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Split GTF by condition using transcript summary table with CPMs.")
    parser.add_argument("-s", "--summary", required=True, help="Transcript summary TSV with Index, Gene, avg_CPM_WT, avg_CPM_Q157R")
    parser.add_argument("-g", "--gtf", default="03_filter_sqanti/filtered.gtf", help="Input GTF/GFF file (default: filtered.gtf)")
    parser.add_argument("-m", "--output_mutant", required=True, help="Output GTF for Q157R")
    parser.add_argument("-w", "--output_wt", required=True, help="Output GTF for WT")
    return parser.parse_args()

def main():
    args = parse_args()

    # === Load transcript summary and filter to PB isoforms only ===
    df = pd.read_csv(args.summary, sep="\t")
    df = df[df["Index"].str.startswith("PB.")]

    # === Build isoform map: {PBID: {gene, CPMs}} ===
    isoform_map = {}
    for _, row in df.iterrows():
        pbid = row["Index"]
        gene = row["Gene"]
        cpm_wt = row["avg_CPM_WT"]
        cpm_q157r = row["avg_CPM_Q157R"]
        isoform_map[pbid] = {
            "gene": gene,
            "wt_cpm": cpm_wt,
            "q157r_cpm": cpm_q157r
        }

    # === Function to write GTF with renamed transcript IDs ===
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

    # === Create isoform subsets by condition ===
    wt_isoforms = {k: v["wt_cpm"] for k, v in isoform_map.items() if v["wt_cpm"] > 0}
    q157r_isoforms = {k: v["q157r_cpm"] for k, v in isoform_map.items() if v["q157r_cpm"] > 0}

    # === Write to files ===
    write_gtf(q157r_isoforms, args.output_mutant)
    write_gtf(wt_isoforms, args.output_wt)

    print(f"Wrote {len(q157r_isoforms)} Q157R transcripts to {args.output_mutant}")
    print(f"Wrote {len(wt_isoforms)} WT transcripts to {args.output_wt}")

if __name__ == "__main__":
    main()