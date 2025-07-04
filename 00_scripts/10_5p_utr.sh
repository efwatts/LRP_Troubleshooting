#!/bin/bash

#SBATCH --job-name=10_5p_utr
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=4:00:00 #amount of time for the whole job
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

conda activate utr

python 00_scripts/10_1_get_gc_exon_and_5utr_info.py \
--gencode_gtf /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
--odir 10_5p_utr

# condition 1
python 00_scripts/10_2_classify_5utr_status.py \
--gencode_exons_bed 10_5p_utr/gencode_exons_for_cds_containing_ensts.bed \
--gencode_exons_chain 10_5p_utr/gc_exon_chain_strings_for_cds_containing_transcripts.tsv \
--sample_cds_gtf 07_make_cds_gtf/condition1_cds.gtf \
--odir 10_5p_utr 

python 00_scripts/10_3_merge_5utr_info_to_pclass_table.py \
--name condition1 \
--utr_info 10_5p_utr/pb_5utr_categories.tsv \
--sqanti_protein_classification 09_sqanti_protein/condition1.sqanti_protein_classification.tsv \
--odir 10_5p_utr

# condition 2
python 00_scripts/10_2_classify_5utr_status.py \
--gencode_exons_bed 10_5p_utr/gencode_exons_for_cds_containing_ensts.bed \
--gencode_exons_chain 10_5p_utr/gc_exon_chain_strings_for_cds_containing_transcripts.tsv \
--sample_cds_gtf 07_make_cds_gtf/condition2_cds.gtf \
--odir 10_5p_utr 

python 00_scripts/10_3_merge_5utr_info_to_pclass_table.py \
--name condition2 \
--utr_info 10_5p_utr/pb_5utr_categories.tsv \
--sqanti_protein_classification 09_sqanti_protein/condition1.sqanti_protein_classification.tsv \
--odir 10_5p_utr

conda deactivate
module purge