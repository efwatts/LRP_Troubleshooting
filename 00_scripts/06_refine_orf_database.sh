#!/bin/bash

#SBATCH --job-name=06_refine_orf_database
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

module load apptainer/1.3.4
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

source $(conda info --base)/etc/profile.d/conda.sh

conda activate refined-database-generation

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

