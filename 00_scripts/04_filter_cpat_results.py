
#!/usr/bin/env python3

import argparse
import pandas as pd
from Bio import SeqIO
import os

def main():
    parser = argparse.ArgumentParser(description="Filter CPAT output and generate filtered/dropout FASTA and TSV files.")
    parser.add_argument("--cpat_output", required=True, help="Path to CPAT output file (TSV format).")
    parser.add_argument("--input_fasta", required=True, help="FASTA file used for CPAT input.")
    parser.add_argument("--output_dir", required=True, help="Directory to write filtered and dropout outputs.")
    parser.add_argument("--prefix", default="filtered", help="Prefix for output files.")
    parser.add_argument("--threshold", type=float, default=0.364, help="Coding probability threshold for filtering.")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    df = pd.read_csv(args.cpat_output, sep="\t")
    coding_df = df[df["Coding_prob"] >= args.threshold]
    dropout_df = df[df["Coding_prob"] < args.threshold]

    coding_ids = set(coding_df["ID"])
    dropout_ids = set(dropout_df["ID"])

    coding_df.to_csv(os.path.join(args.output_dir, f"{args.prefix}_cpat.tsv"), sep="\t", index=False)
    dropout_df.to_csv(os.path.join(args.output_dir, f"dropout_{args.prefix}_cpat.tsv"), sep="\t", index=False)

    with open(os.path.join(args.output_dir, f"{args.prefix}_cpat.fasta"), "w") as coding_out:
        for record in SeqIO.parse(args.input_fasta, "fasta"):
            if record.id in coding_ids:
                SeqIO.write(record, coding_out, "fasta")

    with open(os.path.join(args.output_dir, f"dropout_{args.prefix}_cpat.fasta"), "w") as dropout_out:
        for record in SeqIO.parse(args.input_fasta, "fasta"):
            if record.id in dropout_ids:
                SeqIO.write(record, dropout_out, "fasta")

    print(f"CPAT filtering complete. {len(coding_ids)} coding, {len(dropout_ids)} dropped.")

if __name__ == "__main__":
    main()
