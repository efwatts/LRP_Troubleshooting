#!/bin/bash

#SBATCH --job-name=06_refine_orf_database
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=your_account_name #the account to charge the job to
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=your_email #your email address to receive notifications

module load apptainer/1.3.4
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

source $(conda info --base)/etc/profile.d/conda.sh

conda activate refined-database-generation

# Q157R
python 00_scripts/06_refine_orf_database.py \
--name 06_refine_orf_database/Q157R_0 \
--orfs 05_orf_calling/best_ORF_Q157R.tsv \
--pb_fasta 03_filter_sqanti/MDS_corrected.5degfilter.fasta \
--coding_score_cutoff 0

# WT
python 00_scripts/06_refine_orf_database.py \
--name 06_refine_orf_database/WT_0 \
--orfs 05_orf_calling/best_ORF_WT.tsv \
--pb_fasta 03_filter_sqanti/MDS_corrected.5degfilter.fasta \
--coding_score_cutoff 0

## Create protein-level counts matrix (I am using WT here, but the entries should be the same for Q157R)
# This will create a matrix of protein counts for each sample, which can be used for further analysis.
python 00_scripts/06_protein_counts_matrix.py \
  --sqanti 03_filter_sqanti/MDS_classification.5degfilter.tsv \
  --orfs 06_refine_orf_database/WT_0_orf_refined.tsv \
  --output 06_refine_orf_database/protein_counts_matrix.csv


conda deactivate 

