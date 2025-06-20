from gtfparse import read_gtf
import multiprocessing
from collections import defaultdict
import argparse
from Bio import SeqIO
import pandas as pd
import numpy as np
import logging
import itertools

def is_orf_called_with_stop_codon(orf_fasta, stop_codons=('TAG','TAA','TGA')):  
    """Determines if orf was called with a stop codon as determined by CPAT
    stop codon is True if last codon is in tuple of stop_codons used.

    Args:
        orf_fasta (str): filename of orf fasta file
        stop_codons (tuple, optional): stop codons to use in check. Defaults to ('TAG','TAA','TGA').

    Returns:
        pandas DataFrame: columns:[ID (str), has_stop_codon (bool)]
    """
    orf_stop_codon_status_list = []
    for record in SeqIO.parse(orf_fasta, 'fasta'):
        orf_stop_codon_status_list.append([record.id,str(record.seq).endswith(stop_codons)])
    orf_stop_codon_status = pd.DataFrame(orf_stop_codon_status_list, columns=['ID','has_stop_codon'])
    return orf_stop_codon_status

def orf_mapping(orf_coord, gencode, sample_gtf, orf_seq, pool, num_cores = 12):
    def get_num_upstream_atgs(row):
        orf_start = int(row['orf_start'])
        acc = row['pb_acc']
        if acc in orf_seq.keys():
            seq = orf_seq[acc] 
        else:
            return np.inf
        upstream_seq = seq[0:orf_start-1] # sequence up to the predicted ATG
        num_atgs = upstream_seq.count('ATG')
        return num_atgs

    print(sample_gtf.head())

    exons = sample_gtf[sample_gtf['feature'] == 'exon'].copy()
    #exons = sample_gtf.filter(sample_gtf['feature'] == 'exon').clone()
    exons['exon_length'] = abs(exons['end'] - exons['start']) + 1
   # exons = exons.with_columns([
   # ('exon_length', abs(exons['end'] - exons['start']) + 1)
   # ])
    exons.rename(columns = {'start' : 'exon_start', 'end': 'exon_end'}, inplace = True)
    #exons = exons.rename({'start': 'exon_start', 'end': 'exon_end'})
    print(gencode['feature'].unique())
    start_codons = gencode[gencode['feature'] == 'start_codon']
    start_codons = start_codons[['seqname','transcript_id','strand',  'start', 'end']].copy()
    start_codons.rename(columns = {'start' : 'start_codon_start', 'end': 'start_codon_end'}, inplace = True)
        
    logging.info("Mapping plus strands...")
    plus = plus_mapping(exons, orf_coord, start_codons, pool, num_cores)
    logging.info("Mapping minus strands...")
    minus = minus_mapping(exons, orf_coord, start_codons, pool, num_cores)
    all_cds = pd.concat([plus, minus])
    
    all_cds['upstream_atgs'] = all_cds.apply(get_num_upstream_atgs, axis=1)
    return all_cds

def compare_start_plus(row, start_codons):
    start = int(row['cds_start'])
    match = start_codons[start_codons['start_codon_start'] == start]
    if len(match) > 0:
        return list(match['transcript_id'])
    return None

def plus_mapping_single_chromosome(orf_coord, plus_exons, start_codons):
    plus_exons['current_size'] = plus_exons.sort_values(by = ['transcript_id', 'exon_start']).groupby('transcript_id')['exon_length'].cumsum()
    plus_exons['prior_size'] = plus_exons['current_size'] - plus_exons['exon_length']
    orf_exons = pd.merge(orf_coord, plus_exons, left_on = 'pb_acc', right_on = 'transcript_id', how = 'inner')
    orf_exons = orf_exons[(orf_exons['prior_size'] <= orf_exons['orf_start']) &  (orf_exons['orf_start'] <= orf_exons['current_size'])]
    if len(orf_exons) ==0 :
        logging.warning("no coding start found")
        return orf_exons
    orf_exons['start_diff'] = orf_exons['orf_start'] - orf_exons['prior_size']
    orf_exons['cds_start'] = orf_exons['exon_start'] + orf_exons['start_diff'] - 1
    orf_exons['gencode_atg'] = orf_exons.apply(lambda row : compare_start_plus(row, start_codons), axis = 1)
    orf_exons.drop(columns=['exon_length', 'current_size', 'prior_size', 'start_diff'], inplace = True)
    return orf_exons

def plus_mapping(exons, orf_coord, start_codons, pool, num_cores = 12):

    plus_exons = exons[exons['strand'] == '+'].copy()
    start_codons = start_codons[start_codons['strand'] == '+']
    
    orf_chromosomes = plus_exons['seqname'].unique()
    ref_chromosomes = start_codons['seqname'].unique()
    
    accession_map = plus_exons.groupby('seqname')['transcript_id'].apply(list).to_dict()
    orf_coord_list = [orf_coord[orf_coord['pb_acc'].isin(accession_map[csome])].copy() for csome in orf_chromosomes]
    exon_list = [plus_exons[plus_exons['seqname'] == csome].copy() for csome in orf_chromosomes]
    
    start_codon_list = []
    for csome in orf_chromosomes:
        if csome in ref_chromosomes:
            start_codon_list.append(start_codons[start_codons['seqname'] == csome].copy())
        else:
            start_codon_list.append(start_codons.head())
                                                 
    # pool = multiprocessing.Pool(processes = num_cores)
    iterable = zip(orf_coord_list, exon_list, start_codon_list)
    plus_orf_list = pool.starmap(plus_mapping_single_chromosome, iterable)

    if len(plus_orf_list) > 0:
        plus_orfs = pd.concat(plus_orf_list)
    else:
        plus_orfs = pd.DataFrame(columns = orf_coord.columns)
    
    return plus_orfs
    
def compare_start_minus(row, start_codons):
    start = int(row['cds_start'])
    match = start_codons[(start_codons['start_codon_end'] == start) ]
    if len(match) > 0:
        return list(match['transcript_id'])
    return None

def minus_mapping_single_chromosome(orf_coord, minus_exons, start_codons):
    
    minus_exons['current_size'] = minus_exons.sort_values(by = ['transcript_id', 'exon_start'], ascending=[True,False]).groupby('transcript_id')['exon_length'].cumsum()
    minus_exons['prior_size'] = minus_exons['current_size'] - minus_exons['exon_length']
    orf_exons = pd.merge(orf_coord, minus_exons, left_on = 'pb_acc', right_on = 'transcript_id', how = 'inner')
    orf_exons = orf_exons[orf_exons['orf_start'].between(orf_exons['prior_size'],orf_exons['current_size'])]
    if len(orf_exons) == 0:
        logging.warning("No orf start codons found...")
        return orf_exons
    orf_exons['start_diff'] = orf_exons['orf_start'] - orf_exons['prior_size']
    orf_exons['cds_start'] = orf_exons['exon_end'] - orf_exons['start_diff'] + 1
    orf_exons['gencode_atg'] = orf_exons.apply(lambda row : compare_start_minus(row, start_codons), axis = 1)
    orf_exons.drop(columns=['exon_length', 'current_size', 'prior_size', 'start_diff'], inplace = True)
    return orf_exons

def minus_mapping(exons, orf_coord, start_codons, pool, num_cores = 12):
    minus_exons = exons[exons['strand'] == '-'].copy()
    start_codons = start_codons[start_codons['strand'] == '-'].copy()
        
    orf_chromosomes = minus_exons['seqname'].unique()
    ref_chromosomes = start_codons['seqname'].unique()
    
    accession_map = minus_exons.groupby('seqname')['transcript_id'].apply(list).to_dict()
    orf_coord_list = [orf_coord[orf_coord['pb_acc'].isin(accession_map[csome])].copy() for csome in orf_chromosomes]
    exon_list = [minus_exons[minus_exons['seqname'] == csome].copy() for csome in orf_chromosomes]
    
    start_codon_list = []
    for csome in orf_chromosomes:
        if csome in ref_chromosomes:
            start_codon_list.append(start_codons[start_codons['seqname'] == csome].copy())
        else:
            start_codon_list.append(start_codons.head())
            
    
    iterable = zip(orf_coord_list,exon_list, start_codon_list)    
    # pool = multiprocessing.Pool(processes = num_cores)
    minus_orf_list = pool.starmap(minus_mapping_single_chromosome, iterable)
    if len(minus_orf_list) > 0:
        minus_orfs = pd.concat(minus_orf_list)
    else: 
        minus_orfs = pd.DataFrame(columns = orf_coord.columns)
    return minus_orfs

def read_orf(filename):
    """
    Reads the ORF file and formats the column names
    Keep only predictions with score higher than protein-coding threshold

    Parameters
    ---------
    filename : str
        location of orf coordinate file

    Returns
    --------
    orf: pandas DataFrame
    """
    orf = pd.read_csv(filename, sep = '\t')
    orf[['pb_acc', 'misc', 'orf']] = orf['ID'].str.split('_', expand=True)
    orf['pb_acc'] = orf['pb_acc'].str.split('|').str[0]
    orf = orf.drop(labels=['misc',], axis=1)
    orf.columns = ['ID','len', 'orf_strand', 'orf_frame', 'orf_start', 'orf_end', 'orf_len', 'fickett', 'hexamer', 'coding_score', 'pb_acc', 'orf_rank',]
    logging.info(f"ORF file read \n{orf.head()}")
    return orf

def orf_calling(orf, num_orfs_per_accession = 1):
    """
    Choose 'best' ORF by examining number of upstream ATG's, match to Gencode Transcript start, and ORF codings
    If a gencode start codon matches an orf, choose the ORF that matches Gencode with the least upstream ATGs
    """
    def call_orf(acc_orfs):
        score_threshold = 0.364
        def calling_confidence(row):
            if row['atg_rank'] == 1 and row['score_rank'] == 1:
                return 'Clear Best ORF'
            elif row['coding_score'] <= score_threshold:
                return 'Low Quality ORF'
            else:
                return 'Plausible ORF'
        
        acc_orfs['atg_rank'] = acc_orfs['upstream_atgs'].rank(ascending=True)
        acc_orfs['score_rank'] = acc_orfs['coding_score'].rank(ascending=False)
        acc_orfs['orf_calling_confidence'] = acc_orfs.apply(lambda row : calling_confidence(row), axis = 1)
        
        with_gencode = acc_orfs.dropna(subset=['gencode_atg'])
        # if start codons match a gencode start, take the gencode with the earliest start codon
        if len(with_gencode) >= 1:
            return (with_gencode
                    .sort_values(by='upstream_atgs')
                    .reset_index(drop=True)
                    .head(num_orfs_per_accession)
            )
        else:
            # if no gencode start exists return ORF with best orf_score
            return (
                acc_orfs
                    .sort_values(by='orf_score', ascending=False)
                    .reset_index(drop=True)
                    .head(num_orfs_per_accession)
            )
    atg_shift = 10       # how much to shift sigmoid for atg score
    atg_growth = 0.5    # how quickly the slope of the sigmoid changes 
    orf['atg_score'] = orf['upstream_atgs'].apply(lambda x : 1 - 1/( 1+ np.exp(-atg_growth*(x - atg_shift))))
    # orf['orf_score'] = orf.apply(lambda row: 1 - (1-row['coding_score']*0.99)*(1-row['atg_score']), axis = 1)
    orf['orf_score'] = orf['coding_score']*orf['atg_score']  
    called_orf = orf.groupby('pb_acc').apply(call_orf).reset_index(drop=True)

    return called_orf

def orf_calling_multiprocessing(orf, pool, num_orfs_per_accession=1, num_cores = 12):
    chromosomes = orf['seqname'].unique()
    orf_split = [orf[orf['seqname'] == csome] for csome in chromosomes]
    num_orfs_iter = itertools.repeat(num_orfs_per_accession)
    iterable = zip(orf_split, num_orfs_iter)
    # pool = multiprocessing.Pool(processes = num_cores)
    called_orf_list = pool.starmap(orf_calling, iterable)
    called_orf = pd.concat(called_orf_list)
    return called_orf

def main():
    parser = argparse.ArgumentParser(description='Process ORF related file locations')
    parser.add_argument('--orf_coord', '-oc', required=True)
    parser.add_argument('--orf_fasta', '-of', required=True)
    parser.add_argument('--gencode_gtf', '-g', required=True)
    parser.add_argument('--sample_gtf', '-sg', required=True)
    parser.add_argument('--pb_gene', '-pg', required=True)
    parser.add_argument('--classification', '-c', required=True)
    parser.add_argument('--sample_fasta', '-sf', required=True)
    parser.add_argument('--num_cores', type=int, default=12)
    parser.add_argument('--output_mutant', '-om', required=True)
    parser.add_argument('--output_wt', '-ow', required=True)
    parser.add_argument('--mutant_cols', required=True, help="Comma-separated list of FL columns for mutant samples")
    parser.add_argument('--wt_cols', required=True, help="Comma-separated list of FL columns for wild-type samples")
    results = parser.parse_args()

    mutant_fl_columns = results.mutant_cols.split(',')
    wt_fl_columns = results.wt_cols.split(',')

    pool = multiprocessing.Pool(processes=results.num_cores)

    logging.info("Loading data...")
    orf_coord = read_orf(results.orf_coord)
    is_with_stop_codon = is_orf_called_with_stop_codon(results.orf_fasta)
    orf_coord = pd.merge(orf_coord, is_with_stop_codon, on='ID', how='left')

    gencode = read_gtf(results.gencode_gtf)
    sample_gtf = read_gtf(results.sample_gtf)
    pb_gene = pd.read_csv(results.pb_gene, sep='\t')
    classification = pd.read_csv(results.classification, sep='\t')

    orf_seq = {rec.id.split('|')[0]: str(rec.seq) for rec in SeqIO.parse(results.sample_fasta, 'fasta')}

    logging.info("Mapping orfs to gencode...")
    all_orfs = orf_mapping(orf_coord, gencode, sample_gtf, orf_seq, pool, results.num_cores)
    all_orfs.to_csv('all_orfs_mapped.tsv', sep='\t', index=False)

    logging.info("Calling ORFs...")
    orfs = orf_calling_multiprocessing(all_orfs, pool, 1, results.num_cores)

    logging.info("Adding metadata...")
    mutant_classification = classification.copy()
    mutant_classification['FL'] = mutant_classification[mutant_fl_columns].mean(axis=1)
    total_mutant_fl = mutant_classification['FL'].sum()
    mutant_classification['CPM'] = mutant_classification['FL'] / total_mutant_fl * 1e6

    mutant_orfs = pd.merge(orfs, pb_gene, on='pb_acc', how='left')
    mutant_orfs = pd.merge(mutant_orfs, mutant_classification[['isoform'] + mutant_fl_columns + ['FL', 'CPM']],
                           left_on='pb_acc', right_on='isoform', how='left').drop(columns=['isoform'])

    wt_classification = classification.copy()
    wt_classification['FL'] = wt_classification[wt_fl_columns].mean(axis=1)
    total_wt_fl = wt_classification['FL'].sum()
    wt_classification['CPM'] = wt_classification['FL'] / total_wt_fl * 1e6

    wt_orfs = pd.merge(orfs, pb_gene, on='pb_acc', how='left')
    wt_orfs = pd.merge(wt_orfs, wt_classification[['isoform'] + wt_fl_columns + ['FL', 'CPM']],
                       left_on='pb_acc', right_on='isoform', how='left').drop(columns=['isoform'])

    logging.info("Saving results...")
    columns_to_save = [col for col in orfs.columns if col in mutant_orfs.columns]
    columns_to_save += ['gene', 'FL', 'CPM', 'has_stop_codon']

    mutant_orfs[columns_to_save].to_csv(results.output_mutant, index=False, sep="\t")
    wt_orfs[columns_to_save].to_csv(results.output_wt, index=False, sep="\t")

if __name__ == "__main__":
    main()