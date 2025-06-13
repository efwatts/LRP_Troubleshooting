# Refine ORF Database
Refine the database of ORFs created in the [05 ORF-calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling) based on a user-assigned threshold.<br />
- Filters ORF database to only include accessions with a CPAT coding score above a threshold (default 0.0)
- Filters ORFs to only include ORFs that have a stop codon
- Collapses transcripts that produce the same protein into one entry, keeping a base accession (first alphanumeric).
- Abundances of transcripts (CPM) are collapsed during this process.

Here is an AI generated summary of this step: <br />
> The `refine_orf_database.py` script is designed to refine a database of open reading frames (ORFs) based on user-defined criteria. It takes as input a list of ORFs, their corresponding sequences, and a coding score cutoff. The script filters the ORFs to retain only those with a coding score above the specified cutoff and ensures that each ORF has a stop codon. Additionally, it collapses transcripts that produce the same protein into a single entry, retaining the first alphanumeric accession. The output includes refined ORF sequences and a summary table.
> The script generates two output files: a FASTA file containing the refined ORF sequences and a TSV file summarizing the refined ORF database.
## Input files
- `best_ORF.tsv` - ORF database from the [05 ORF-calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling)
- `corrected.5degfilter.fasta` - FASTA file from the [03_filter_sqanti module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti)
- `coding_score_cutoff` - User-defined cutoff for coding score (default 0.0)
## Output files
- `scorecutoff_orf_refined.fasta` - Refined ORF sequences in FASTA format
- `scorecutoff_orf_refined.tsv` - Summary table of refined ORFs with their coding scores and other relevant information
- `protein_counts_matrix.csv` - an aggregated matrix of raw protein counts for each ORF, with ORFs that produce the same protein collapsed into one entry. The first alphanumeric accession is kept as the base accession.

We also added a dropout module to the script to record which isoforms drop out. <br />

## Required installations
Load modules (if on HPC) and create and activate conda environment. <br />
```
module load apptainer/1.2.2
module load gcc/11.4.0
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda env create -f ./00_environments/06_refine_orf_database.yml
conda activate refined-database-generation
```

## Run ORF calling from a SLURM script
```
sbatch 00_scripts/06_refine_orf_database.sh
```
## Or run these commands.
```
# condition1
python 00_scripts/06_refine_orf_database.py \
--name 06_refine_orf_database/condition1_0 \
--orfs 05_orf_calling/best_ORF_condition1.tsv \
--pb_fasta 03_filter_sqanti/sample_corrected.5degfilter.fasta \
--coding_score_cutoff 0

# condition2
python 00_scripts/06_refine_orf_database.py \
--name 06_refine_orf_database/condition2_0 \
--orfs 05_orf_calling/best_ORF_condition2.tsv \
--pb_fasta 03_filter_sqanti/sample_corrected.5degfilter.fasta \
--coding_score_cutoff 0

conda deactivate 
module purge
```
## Proceed to [07_make_cds_gtf module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_make_cds_gtf)
