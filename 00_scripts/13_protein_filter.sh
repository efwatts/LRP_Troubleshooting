#!/bin/bash

#SBATCH --job-name=13_protein_filter
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=your_account_name #the account to charge the job to
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=your_email #your email address to receive notifications

module load gcc
module load openmpi
module load python
module load miniforge

source $(conda info --base)/etc/profile.d/conda.sh

conda activate protein_class

# condition 1
python 00_scripts/13_protein_filter.py \
--protein_classification 11_protein_classification/condition1.protein_classification.tsv \
--gencode_gtf /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
--protein_fasta 12_protein_gene_rename/condition1.protein_refined.fasta \
--sample_cds_gtf 12_protein_gene_rename/condition1_with_cds_refined.gtf \
--min_junctions_after_stop_codon 2 \
--name 13_protein_filter/condition1

# condition 2
python 00_scripts/13_protein_filter.py \
--protein_classification 11_protein_classification/condition2.protein_classification.tsv \
--gencode_gtf /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
--protein_fasta 12_protein_gene_rename/condition2.protein_refined.fasta \
--sample_cds_gtf 12_protein_gene_rename/condition2_with_cds_refined.gtf \
--min_junctions_after_stop_codon 2 \
--name 13_protein_filter/condition2

conda deactivate
module purge