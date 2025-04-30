
#!/usr/bin/env python3

import pandas as pd
from Bio import SeqIO
from Bio import Seq
from collections import defaultdict
import argparse
import logging
import os

def get_accession_seqs(seqs):
    logging.info('Getting accession sequences...')
    pb_seqs = {}
    redundant_accs = []
    for entry in seqs:
        seq = str(entry.seq)
        pb_acc = entry.id.split('|')[0]
        if pb_acc in pb_seqs:
            redundant_accs.append(pb_acc)
        else:
            pb_seqs[pb_acc] = seq
    return pb_seqs, redundant_accs

def combine_by_sequence(orfs, pb_seqs):
    logging.info('Combining by sequence...')
    orfs = orfs[['pb_acc', 'orf_start', 'orf_end', 'orf_len']]
    pb_pseqs = defaultdict(list)
    for _, row in orfs.iterrows():
        pb_acc, start, end, _ = row
        seq = pb_seqs.get(pb_acc)
        if seq:
            orf_seq = seq[start-1:end]
            prot_seq = Seq.translate(orf_seq, to_stop=True)
            pb_pseqs[prot_seq].append(pb_acc)
    return pb_pseqs

def order_pb_acc_numerically(accs):
    accs_numerical = []
    for acc in accs:
        try:
            _, gene_idx, iso_idx = acc.split('.')
            accs_numerical.append((int(gene_idx), int(iso_idx)))
        except:
            continue
    accs_numerical.sort()
    return [f"PB.{g}.{i}" for g, i in accs_numerical]

def filter_orf_scores_and_stopcodon(orfs, cutoff):
    logging.info(f'Filtering ORFs with coding_score >= {cutoff} and requiring a stop codon...')
    kept_orfs = orfs[(orfs["coding_score"] >= cutoff) & (orfs["has_stop_codon"])]
    dropout_orfs = orfs[~((orfs["coding_score"] >= cutoff) & (orfs["has_stop_codon"]))]
    return kept_orfs, dropout_orfs

def write_dropout_files(dropout_ids, input_fasta, dropout_orfs, output_prefix):
    dropout_fasta = f"{os.path.dirname(output_prefix)}/dropout_{os.path.basename(output_prefix)}_orf.fasta"
    dropout_tsv = f"{os.path.dirname(output_prefix)}/dropout_{os.path.basename(output_prefix)}_orf.tsv"

    with open(dropout_fasta, "w") as out_f:
        for record in SeqIO.parse(input_fasta, "fasta"):
            if record.id.split("|")[0] in dropout_ids:
                SeqIO.write(record, out_f, "fasta")

    dropout_orfs.to_csv(dropout_tsv, sep="\t", index=False)

def main():
    parser = argparse.ArgumentParser(description="Refine ORF database with dropout tracking (pipeline style).")
    parser.add_argument('--name', required=True, help='Full output prefix including directory, e.g., 06_refine_orf_database/Sample6_0')
    parser.add_argument('--orfs', required=True, help='Input ORF coordinate file.')
    parser.add_argument('--pb_fasta', required=True, help='Input PacBio transcript FASTA file.')
    parser.add_argument('--coding_score_cutoff', type=float, default=0.0, help='CPAT coding score cutoff.')

    args = parser.parse_args()
    output_prefix = args.name

    logging.info("Reading input files...")
    orfs = pd.read_table(args.orfs)
    all_ids = set(orfs["pb_acc"])

    # Filter based on coding score and stop codon
    orfs_filtered, orfs_dropout = filter_orf_scores_and_stopcodon(orfs, args.coding_score_cutoff)

    kept_ids = set(orfs_filtered["pb_acc"])
    dropout_ids = all_ids - kept_ids

    # Save dropouts
    write_dropout_files(dropout_ids, args.pb_fasta, orfs_dropout, output_prefix)

    seqs = SeqIO.parse(open(args.pb_fasta), "fasta")
    pb_seqs, _ = get_accession_seqs(seqs)
    pb_pseqs = combine_by_sequence(orfs_filtered, pb_seqs)

    combined_tsv = f"{output_prefix}_combined.tsv"
    combined_fasta = f"{output_prefix}_combined.fasta"

    with open(combined_tsv, "w") as ofile, open(combined_fasta, "w") as ofile2:
        ofile.write("protein_sequence\tpb_accs\n")
        for seq, accs in pb_pseqs.items():
            accs_sorted = order_pb_acc_numerically(accs)
            accs_str = "|".join(accs_sorted)
            ofile.write(seq + "\t" + accs_str + "\n")
            ofile2.write(">" + accs_str + "\n" + seq + "\n")

    pacbio = pd.read_csv(combined_tsv, sep="\t")
    seqs = SeqIO.parse(open(combined_fasta), "fasta")
    os.remove(combined_tsv)
    os.remove(combined_fasta)

    pacbio["accessions"] = pacbio["pb_accs"].str.split("|")
    pacbio["base_acc"] = pacbio["accessions"].apply(lambda x: x[0])

    fl_dict = pd.Series(orfs_filtered.FL.values, index=orfs_filtered.pb_acc).to_dict()
    cpm_dict = pd.Series(orfs_filtered.CPM.values, index=orfs_filtered.pb_acc).to_dict()

    def get_total(accessions, score_dict):
        return sum(score_dict.get(acc, 0) for acc in accessions)

    pacbio["FL"] = pacbio["accessions"].apply(lambda accs: get_total(accs, fl_dict))
    pacbio["CPM"] = pacbio["accessions"].apply(lambda accs: get_total(accs, cpm_dict))

    orfs_filtered = orfs_filtered[["pb_acc", "coding_score", "orf_score", "orf_calling_confidence", "upstream_atgs", "gene"]]
    pacbio = pd.merge(pacbio, orfs_filtered, how="inner", left_on="base_acc", right_on="pb_acc")

    pb_gene = pd.Series(orfs_filtered.gene.values, index=orfs_filtered.pb_acc).to_dict()
    base_map = pd.Series(pacbio.base_acc.values, index=pacbio.pb_accs).to_dict()

    refined_fasta = f"{output_prefix}_orf_refined.fasta"
    with open(refined_fasta, "w") as ofile:
        for entry in seqs:
            seq = str(entry.seq)
            pb_acc = entry.id
            base_acc = base_map.get(pb_acc, pb_acc)
            gene = pb_gene.get(base_acc, "NA")
            ofile.write(f">pb|{base_acc}|fullname GN={gene}\n{seq}\n")

    refined_tsv = f"{output_prefix}_orf_refined.tsv"
    pacbio = pacbio[["pb_accs", "base_acc", "coding_score", "orf_calling_confidence",
                     "upstream_atgs", "orf_score", "gene", "FL", "CPM"]]
    pacbio.to_csv(refined_tsv, sep="\t", index=False)

    logging.info("ORF refinement complete with dropout tracking (pipeline style).")

if __name__ == "__main__":
    main()
