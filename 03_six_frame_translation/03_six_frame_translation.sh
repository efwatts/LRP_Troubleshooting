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
module purge
module load gcc/11.4.0
module load mamba/22.11.1-4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11
module load openmpi/4.1.4
module load python/3.11.4

cd /project/sheynkman/users/emily/LRP_test/jurkat

conda activate 6frame

python ./00_scripts/03_six_frame_translation.py \
--iso_annot ./02_sqanti/output/jurkat_classification.txt \
--ensg_gene ./01_reference_tables/ensg_gene.tsv \
--sample_fasta ./02_sqanti/output/jurkat_corrected.fasta \
--output_fasta ./03_six_frame_translation/pacbio_6frm_database_gene_grouped.fasta

conda deactivate
