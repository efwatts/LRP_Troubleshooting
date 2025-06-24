#!/bin/bash

#SBATCH --job-name=04_transcriptome_summary
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=your_account_name #the account to charge the job to
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=your_email #your email address to receive notifications

# Load necessary modules (if needed)
module purge
module load gcc
module load miniforge
module load openmpi
module load python

conda activate transcriptome_sum

python 00_scripts/04_transcriptome_summary_gene_table_only.py \
--sq_out 03_filter_sqanti/sample_collapsed_classification.tsv \
--ensg_to_gene 01_reference_tables/ensg_gene.tsv \
--enst_to_isoname 01_reference_tables/enst_isoname.tsv \
--odir 04_transcriptome_summary/ 

conda deactivate
module purge