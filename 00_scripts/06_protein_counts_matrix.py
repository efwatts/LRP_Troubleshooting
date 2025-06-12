#!/usr/bin/env python3

import pandas as pd
from collections import defaultdict
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Create protein-level counts matrix from SQANTI and ORF collapse info")
    parser.add_argument("--sqanti", required=True, help="SQANTI classification table with FL.sample columns")
    parser.add_argument("--orfs", required=True, help="Refined ORF table with pb_accs and base_acc columns")
    parser.add_argument("--output", required=True, help="Output counts matrix CSV")
    return parser.parse_args()

def main():
    args = parse_args()

    # Load input files
    sqanti = pd.read_csv(args.sqanti, sep="\t")
    orf_table = pd.read_csv(args.orfs, sep="\t")

    # Extract FL sample columns
    fl_cols = [col for col in sqanti.columns if col.startswith("FL.")]
    fl_sample_names = [col.replace("FL.", "") for col in fl_cols]

    # Create a map: PB accession → sample FLs
    sqanti_fl = sqanti.set_index("isoform")[fl_cols]
    pb_to_fl = sqanti_fl.fillna(0)

    # Create protein groupings
    protein_groups = {}  # key: output protein ID, value: list of PB accessions
    for i, row in orf_table.iterrows():
        group_id = row["base_acc"]
        pb_accs = row["pb_accs"].split("|")
        protein_groups[group_id] = pb_accs

    # Summarize FL counts per group
    output_rows = []
    for group_id, accessions in protein_groups.items():
        sample_counts = [0] * len(fl_cols)
        for acc in accessions:
            if acc in pb_to_fl.index:
                sample_counts = [x + y for x, y in zip(sample_counts, pb_to_fl.loc[acc])]
        row = [group_id] + sample_counts
        output_rows.append(row)

    # Output DataFrame
    output_df = pd.DataFrame(output_rows, columns=["id"] + fl_sample_names)
    output_df.to_csv(args.output, index=False)

if __name__ == "__main__":
    main()