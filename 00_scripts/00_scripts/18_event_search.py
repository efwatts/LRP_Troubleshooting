#!/usr/bin/env python3

import re
import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description="Compare rMATS skipped exon to SUPPA SE events")
    parser.add_argument("--ioe", required=True, help="SUPPA all.events.ioe file")
    parser.add_argument("--gene", required=True, help="Gene name to filter (e.g., Ezh2)")
    parser.add_argument("--chrom", required=True, help="Chromosome name (e.g., chr6)")
    parser.add_argument("--strand", required=True, choices=["+", "-"], help="Strand (+ or -)")
    parser.add_argument("--skipped_start", type=int, required=True, help="rMATS skipped exon start")
    parser.add_argument("--skipped_end", type=int, required=True, help="rMATS skipped exon end")
    return parser.parse_args()

def parse_event_coords(event_str):
    """
    Extract coordinates from SUPPA SE event_id string.
    Format example: chr6:47541844-47541970:47542365-47542406:-
    """
    try:
        match = re.match(r"(chr[^:]+):(\d+)-(\d+):(\d+)-(\d+):([+-])", event_str)
        if match:
            return {
                "chr": match.group(1),
                "exon1_start": int(match.group(2)),
                "exon1_end": int(match.group(3)),
                "exon2_start": int(match.group(4)),
                "exon2_end": int(match.group(5)),
                "strand": match.group(6)
            }
    except Exception:
        return None
    return None

def main():
    args = parse_args()

    # Load IOE
    with open(args.ioe) as f:
        lines = f.readlines()

    header = lines[0].strip().split('\t')
    data = [line.strip().split('\t') for line in lines[1:] if line.strip()]
    df = pd.DataFrame(data, columns=header)

    # Filter SE events for the gene
    df = df[(df["event_id"].str.contains("SE")) & (df["gene_id"] == args.gene)]

    matched = []
    for i, row in df.iterrows():
        coords = parse_event_coords(row["event_id"])
        if coords and coords["chr"] == args.chrom and coords["strand"] == args.strand:
            delta_start = abs(coords["exon1_start"] - args.skipped_start)
            delta_end = abs(coords["exon1_end"] - args.skipped_end)
            matched.append({
                "event_id": row["event_id"],
                "gene_id": row["gene_id"],
                "delta_skipped_exon_start": delta_start,
                "delta_skipped_exon_end": delta_end
            })

    if matched:
        result_df = pd.DataFrame(matched)
        print(result_df.to_string(index=False))
    else:
        print("No matching events found for given gene and coordinates.")

if __name__ == "__main__":
    main()