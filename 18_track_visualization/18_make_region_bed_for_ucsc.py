#!/usr/bin/env python3
# code from making custom regions of gencode + pacbio

# %%

import subprocess
import pandas as pd
import os
import argparse
import gtfparse

def make_region_bed_for_ucsc(name, sample_gtf, reference_gtf, output_dir):
    # exon bed ranges of pb
    pb = pd.read_table(sample_gtf, skiprows=1, header=None)
    pb = pb[pb[2] == 'CDS']
    # only move forward with entries with a mapped gene
    pb = pb[~pb[8].str.contains('gene_id "-";')]
    pb = pb[[0, 3, 4]]
    both = pb
    
    if reference_gtf is not None:
        gc = pd.read_table(reference_gtf, skiprows=5, header=None)
        gc = gc[gc[2] == 'exon']
        gc = gc[[0, 3, 4]]
        both = pd.concat([pb, gc])
    
    both.columns = ['chr', 'start', 'end']
    both['start'] = both['start'] - 1

    fn = os.path.join(output_dir, f'{name}_cds_ranges.bed')
    both.to_csv(fn, sep='\t', index=None, header=None)

    # sort bed
    rows = subprocess.getoutput(f'bedtools sort -i {fn}')
    fn_sorted = fn.replace('.bed', '_sorted.bed')

    # subtract 1 from start
    with open(fn_sorted, 'w') as ofile:
        ofile.write(rows)

    # merge ranges
    rows = subprocess.getoutput(f'bedtools merge -i {fn_sorted}')

    # write to file
    with open(os.path.join(output_dir, f"{name}_ucsc_multiregion.bed"), "w") as ofile:
        ofile.write(f'#database hg38\n#shortDesc Exons of isoforms in {name} PacBio CDS\n#padding 10\n')
        ofile.write(rows)

    # clean-up files
    os.remove(fn)
    os.remove(fn_sorted)

def main():
    parser = argparse.ArgumentParser("IO file locations for making region bed")
    parser.add_argument("--name", action="store", dest="name", help="name of sample - used for output file name")
    parser.add_argument("--sample_gtf", action="store", dest="sample_gtf", help="sample gtf with cds. from make_pacbio_cds_gtf")
    parser.add_argument("--reference_gtf", action="store", dest="reference_gtf", help="reference gtf", default="")
    parser.add_argument("--output_dir", action="store", dest="output_dir", help="output directory for the result files", default=".")
    results = parser.parse_args()
    make_region_bed_for_ucsc(results.name, results.sample_gtf, results.reference_gtf, results.output_dir)

if __name__ == "__main__":
    main()



