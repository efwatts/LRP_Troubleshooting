#!/bin/bash

#SBATCH --job-name=11_protein_classification
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

source $(conda info --base)/etc/profile.d/conda.sh

conda activate protein_class

# condition 1
python 00_scripts/11_protein_classification_add_meta.py \
--protein_classification  10_5p_utr/Q157R.sqanti_protein_classification_w_5utr_info.tsv \
--best_orf 05_orf_calling/best_ORF_Q157R.tsv \
--refined_meta 06_refine_orf_database/Q157R_0_orf_refined.tsv \
--ensg_gene 01_reference_tables/ensg_gene.tsv \
--name Q157R \
--dest_dir 11_protein_classification/

python 00_scripts/11_protein_classification.py \
--sqanti_protein 11_protein_classification/Q157R.protein_classification_w_meta.tsv \
--name Q157R \
--dest_dir 11_protein_classification/

# condition 2
python 00_scripts/11_protein_classification_add_meta.py \
--protein_classification  10_5p_utr/WT.sqanti_protein_classification_w_5utr_info.tsv \
--best_orf 05_orf_calling/best_ORF_WT.tsv \
--refined_meta 06_refine_orf_database/WT_0_orf_refined.tsv \
--ensg_gene 01_reference_tables/ensg_gene.tsv \
--name WT \
--dest_dir 11_protein_classification/

python 00_scripts/11_protein_classification.py \
--sqanti_protein 11_protein_classification/WT.protein_classification_w_meta.tsv \
--name WT \
--dest_dir 11_protein_classification/

conda deactivate 
module purge