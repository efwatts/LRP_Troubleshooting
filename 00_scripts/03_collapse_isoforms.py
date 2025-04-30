#!/usr/bin/env python3
#%%
from cupcake.io import GFF
from collections import defaultdict
from cupcake.tofu import compare_junctions
import os
import argparse
from Bio import SeqIO

### helper functions

def can_merge(m, r1, r2, internal_fuzzy_max_dist):
    if m == 'subset':
        r1, r2 = r2, r1
    if m in ['super', 'subset']:
        n2 = len(r2.ref_exons)
        if r1.strand == '+':
            if n2 == 1:
                return r1.ref_exons[-1].start - r2.ref_exons[-1].start <= internal_fuzzy_max_dist
            else:
                return (abs(r1.ref_exons[-1].start - r2.ref_exons[-1].start) <= internal_fuzzy_max_dist and
                        r1.ref_exons[-n2].start <= r2.ref_exons[0].start < r1.ref_exons[-n2].end)
        else:
            if n2 == 1:
                return r1.ref_exons[0].end - r2.ref_exons[0].end >= -internal_fuzzy_max_dist
            else:
                return (abs(r1.ref_exons[0].end - r2.ref_exons[0].end) <= internal_fuzzy_max_dist and
                        r1.ref_exons[n2 - 1].start <= r2.ref_exons[-1].end < r1.ref_exons[n2].end)

def filter_out_subsets(recs, internal_fuzzy_max_dist):
    i = 0
    while i < len(recs) - 1:
        no_change = True
        j = i + 1
        while j < len(recs):
            if recs[j].start > recs[i].end:
                break
            recs[i].segments = recs[i].ref_exons
            recs[j].segments = recs[j].ref_exons
            m = compare_junctions.compare_junctions(recs[i], recs[j], internal_fuzzy_max_dist)
            if can_merge(m, recs[i], recs[j], internal_fuzzy_max_dist):
                if m == 'super':
                    recs.pop(j)
                else:
                    recs.pop(i)
                    no_change = False
            else:
                j += 1
        if no_change:
            i += 1

def modify_gff_file(sqanti_gtf, output_filename):
    if not os.path.exists(output_filename):
        with open(output_filename, 'w') as ofile:
            for line in open(sqanti_gtf):
                pb_acc = line.split('transcript_id "')[1].split('"')[0]
                pb_locus_acc = 'PB.' + pb_acc.split('.')[1]
                wds = line.split('\t')
                if wds[2] in ('transcript', 'exon'):
                    prefix = wds[0:8]
                    acc_line = 'gene_id "{}"; transcript_id "{}";'.format(pb_acc, pb_locus_acc)
                    ofile.write('\t'.join(prefix + [acc_line]) + '\n')

#%%
def collapse_isoforms(gff_filename, fasta_filename, output_dir, name):
    output_gtf_path = os.path.join(output_dir, f"{name}_corrected.5degfilter.gff")
    output_fasta_path = os.path.join(output_dir, f"{name}_corrected.5degfilter.fasta")
    dropout_dir = os.path.join(output_dir, "dropout")
    os.makedirs(dropout_dir, exist_ok=True)

    recs = defaultdict(list)
    reader = GFF.collapseGFFReader(gff_filename)
    for record in reader:
        assert record.seqid.startswith('PB.')
        pb_cluster = f'PB.{record.seqid.split(".")[1]}'
        recs[pb_cluster].append(record)

    good_ids = set()
    with open(output_gtf_path, 'w') as out_gtf:
        for pb_cluster, isoforms in recs.items():
            fuzzy_junc_max_dist = 0
            filter_out_subsets(isoforms, fuzzy_junc_max_dist)
            for record in isoforms:
                GFF.write_collapseGFF_format(out_gtf, record)
                good_ids.add(record.seqid)

    # Write filtered FASTA (only keeping good_ids)
    with open(output_fasta_path, 'w') as out_fasta, \
         open(os.path.join(dropout_dir, f"{name}_dropout.fasta"), 'w') as dropout_fasta:
        for record in SeqIO.parse(fasta_filename, 'fasta'):
            if record.id in good_ids:
                SeqIO.write(record, out_fasta, 'fasta')
            else:
                SeqIO.write(record, dropout_fasta, 'fasta')

    # Write dropout GTF
    with open(gff_filename, 'r') as gtf_in, \
         open(os.path.join(dropout_dir, f"{name}_dropout.gff"), 'w') as dropout_gtf:
        for line in gtf_in:
            if line.startswith("#"):
                continue
            match = re.search(r'transcript_id "([^"]+)"', line)
            if match and match.group(1) not in good_ids:
                dropout_gtf.write(line)

#%%
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', '-oc', required=True)
    parser.add_argument('--sqanti_gtf', required=True)
    parser.add_argument('--sqanti_fasta', required=True)
    parser.add_argument('--output_dir', required=True, help='Output directory for collapsed results.')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    collapse_isoforms(args.sqanti_gtf, args.sqanti_fasta, args.output_dir, args.name)

if __name__ == "__main__":
    main()
