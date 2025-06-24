#!/bin/bash

#SBATCH --job-name=02_gencode_database
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=your_account_name #the account to charge the job to
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=your_email #your email address to receive notifications

module purge 
module load gcc
module load openmpi
module load python
module load miniforge
module load perl
module load star
module load kallisto

source $(conda info --base)/etc/profile.d/conda.sh

conda activate make_database

python 00_scripts/02_make_gencode_database.py \
--gencode_fasta /project/sheynkman/external_data/GENCODE_v47/gencode.v47.pc_transcripts.fa \
--protein_coding_genes 01_reference_tables/protein_coding_genes.txt \
--output_fasta 02_make_gencode_database/gencode_clusters.fasta \
--output_cluster 02_make_gencode_database/gencode_isoname_clusters.tsv

conda deactivate
module purge