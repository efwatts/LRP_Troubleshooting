#!/bin/bash

#SBATCH --job-name=11_protein_classification
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

# condition 1
python 00_scripts/11_protein_classification_add_meta.py \
--protein_classification  10_5p_utr/condition1.sqanti_protein_classification_w_5utr_info.tsv \
--best_orf 05_orf_calling/best_ORF_condition1.tsv \
--refined_meta 06_refine_orf_database/condition1_0_orf_refined.tsv \
--ensg_gene 01_reference_tables/ensg_gene.tsv \
--name condition1 \
--dest_dir 11_protein_classification/

python 00_scripts/11_protein_classification.py \
--sqanti_protein 11_protein_classification/condition1.protein_classification_w_meta.tsv \
--name condition1 \
--dest_dir 11_protein_classification/

# condition 2
python 00_scripts/11_protein_classification_add_meta.py \
--protein_classification  10_5p_utr/condition2.sqanti_protein_classification_w_5utr_info.tsv \
--best_orf 05_orf_calling/best_ORF_condition2.tsv \
--refined_meta 06_refine_orf_database/condition2_0_orf_refined.tsv \
--ensg_gene 01_reference_tables/ensg_gene.tsv \
--name condition2 \
--dest_dir 11_protein_classification/

python 00_scripts/11_protein_classification.py \
--sqanti_protein 11_protein_classification/condition2.protein_classification_w_meta.tsv \
--name condition2 \
--dest_dir 11_protein_classification/

conda deactivate 
module purge