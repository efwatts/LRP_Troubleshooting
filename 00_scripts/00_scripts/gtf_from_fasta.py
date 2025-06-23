#!/usr/bin/env python3

import sys
from Bio import SeqIO

def main(fasta_file, gtf_file, output_file):
    # Step 1: Get IDs from FASTA
    fasta_ids = set(record.id for record in SeqIO.parse(fasta_file, "fasta"))
    
    # Step 2: Extract matching lines from GTF
    with open(gtf_file) as ref, open(output_file, "w") as out:
        for line in ref:
            if line.startswith("#"):
                continue  # skip header/comment lines
            if any(f'transcript_id "{id}"' in line for id in fasta_ids):
                out.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python extract_gtf_from_fasta.py your.fasta your_reference.gtf output_subset.gtf")
        sys.exit(1)
    
    fasta_file = sys.argv[1]
    gtf_file = sys.argv[2]
    output_file = sys.argv[3]
    
    main(fasta_file, gtf_file, output_file)