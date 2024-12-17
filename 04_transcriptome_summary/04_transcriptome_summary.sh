#!/bin/bash

#SBATCH --job-name=six_frame
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

# Load necessary modules (if needed)
module load gcc/11.4.0
module load mamba/22.11.1-4
module load bioconda/py3.10
module load miniforge/24.3.0-py3.11
module load openmpi/4.1.4
module load python/3.11.4

conda activate transcriptome_sum

python ./00_scripts/04_transcriptome_summary.py \
--sq_out ./03_filter_sqanti/jurkat_classification.txt \
--tpm ./00_input_data/jurkat_gene_kallisto.tsv \
--ribo ./00_input_data/kallist_table_rdeplete_jurkat.tsv \
--ensg_to_gene ./01_reference_tables/ensg_gene.tsv \
--enst_to_isoname ./01_reference_tables/enst_isoname.tsv \
--len_stats ./01_reference_tables/gene_lens.tsv \
--odir ./04_transcriptome_summary/

conda deactivate
module purge
