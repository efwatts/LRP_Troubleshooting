#!/bin/bash

#SBATCH --job-name=12_protein_gene_rename
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=your_account_name #the account to charge the job tob
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
python 00_scripts/12_protein_gene_rename.py \
    --sample_gtf 07_make_cds_gtf/condition1_cds.gtf \
    --sample_protein_fasta 06_refine_orf_database/condition1_0_orf_refined.fasta \
    --sample_refined_info 06_refine_orf_database/condition1_0_orf_refined.tsv \
    --pb_protein_genes 11_protein_classification/condition1_genes.tsv \
    --name 12_protein_gene_rename/condition1

# condition 2
python 00_scripts/12_protein_gene_rename.py \
    --sample_gtf 07_make_cds_gtf/condition2_cds.gtf \
    --sample_protein_fasta 06_refine_orf_database/condition2_0_orf_refined.fasta \
    --sample_refined_info 06_refine_orf_database/condition2_0_orf_refined.tsv \
    --pb_protein_genes 11_protein_classification/condition2_genes.tsv \
    --name 12_protein_gene_rename/condition2

conda deactivate
module purge
