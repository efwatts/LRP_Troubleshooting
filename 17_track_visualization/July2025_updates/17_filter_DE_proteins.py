#!/usr/bin/env python3

import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Filter and annotate condition-specific protein GTFs with CPM and gene info.")
    parser.add_argument("-i", "--input", required=True, help="Transcript summary table with CPM values")
    parser.add_argument("--gtf_aml", required=True, help="Input GTF file for AML condition")
    parser.add_argument("--gtf_nbm", required=True, help="Input GTF file for NBM condition")
    parser.add_argument("-a", "--output_aml", required=True, help="Output GTF file for AML")
    parser.add_argument("-n", "--output_nbm", required=True, help="Output GTF file for NBM")
    return parser.parse_args()

def load_isoform_map(summary_file):
    df = pd.read_csv(summary_file, sep="\t")

    # Use 'Index' column if present, otherwise assume first column is PBID
    pb_col = "Index" if "Index" in df.columns else df.columns[0]

    isoform_map = {}
    for _, row in df.iterrows():
        pb_id = str(row[pb_col]).strip()
        gene = row["Gene"]
        aml_cpm = row["avg_CPM_AML"]
        nbm_cpm = row["avg_CPM_NBM"]
        isoform_map[pb_id] = {
            "gene": gene,
            "aml_cpm": aml_cpm,
            "nbm_cpm": nbm_cpm
        }
    return isoform_map

def filter_and_annotate_gtf(input_gtf, output_gtf, isoform_map, condition_key):
    written, skipped_missing, skipped_zero = 0, 0, 0

    with open(input_gtf) as fin, open(output_gtf, "w") as fout:
        for line in fin:
            if line.startswith("#") or line.strip() == "":
                continue
            parts = line.strip().split("\t")
            attr_field = parts[8]

            if 'transcript_id "' not in attr_field:
                continue

            try:
                tid_full = attr_field.split('transcript_id "')[1].split('"')[0]
                pb_id = next((p.strip() for p in tid_full.split("|") if p.strip().startswith("PB.")), None)
                if pb_id is None:
                    skipped_missing += 1
                    continue
            except Exception:
                skipped_missing += 1
                continue

            pb_id_clean = pb_id.strip()
            if pb_id_clean not in isoform_map:
                skipped_missing += 1
                continue

            cpm = isoform_map[pb_id_clean][condition_key]
            if cpm <= 0:
                skipped_zero += 1
                continue

            gene = isoform_map[pb_id_clean]["gene"]
            new_tid = f"{gene}|{pb_id_clean}|{cpm:.6f}"

            parts[1] = "hg38_protein"
            parts[8] = f'gene_id "{gene}"; transcript_id "{new_tid}";'
            fout.write("\t".join(parts) + "\n")
            written += 1

    print(f"Wrote {written} transcripts to {output_gtf}")
    print(f"Skipped {skipped_missing} due to missing PBID in summary table")
    print(f"Skipped {skipped_zero} due to CPM = 0")

def main():
    args = parse_args()
    isoform_map = load_isoform_map(args.input)

    filter_and_annotate_gtf(args.gtf_aml, args.output_aml, isoform_map, "aml_cpm")
    filter_and_annotate_gtf(args.gtf_nbm, args.output_nbm, isoform_map, "nbm_cpm")

if __name__ == "__main__":
    main()