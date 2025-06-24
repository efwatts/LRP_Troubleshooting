#!/bin/bash

#SBATCH --job-name=14_protein_hybrid_database
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=your_account_name #the account to charge the job to
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=your_email #your email address to receive notifications

module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

source $(conda info --base)/etc/profile.d/conda.sh

conda activate protein_class

# Condition 1
python ./00_scripts/14_make_hybrid_database.py \
    --protein_classification 13_protein_filter/condition1.classification_filtered.tsv \
    --gene_lens 01_reference_tables/gene_lens.tsv \
    --pb_fasta 13_protein_filter/condition1.filtered_protein.fasta \
    --gc_fasta 02_make_gencode_database/gencode_clusters.fasta \
    --refined_info 12_protein_gene_rename/condition1_orf_refined_gene_update.tsv \
    --pb_cds_gtf 13_protein_filter/condition1_with_cds_filtered.gtf \
    --name 14_protein_hybrid_database/condition1

# Condition 2
python ./00_scripts/14_make_hybrid_database.py \
    --protein_classification 13_protein_filter/condition2.classification_filtered.tsv \
    --gene_lens 01_reference_tables/gene_lens.tsv \
    --pb_fasta 13_protein_filter/condition2.filtered_protein.fasta \
    --gc_fasta 02_make_gencode_database/gencode_clusters.fasta \
    --refined_info 12_protein_gene_rename/condition2_orf_refined_gene_update.tsv \
    --pb_cds_gtf 13_protein_filter/condition2_with_cds_filtered.gtf \
    --name 14_protein_hybrid_database/condition2

conda deactivate
module purge