#!/bin/bash

#SBATCH --job-name=5p_utr
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11

conda activate utr

# Mother 
python ./00_scripts/10_1_get_gc_exon_and_5utr_info.py \
--gencode_gtf /project/sheynkman/external_data/GENCODE_v46/gencode.v46.basic.annotation.gtf \
--odir mother/10_5p_utr

python ./00_scripts/10_2_classify_5utr_status.py \
--gencode_exons_bed mother/10_5p_utr/gencode_exons_for_cds_containing_ensts.bed \
--gencode_exons_chain mother/10_5p_utr/gc_exon_chain_strings_for_cds_containing_transcripts.tsv \
--sample_cds_gtf mother/07_make_cds_gtf/Mot_cds.gtf \
--odir mother/10_5p_utr 

python ./00_scripts/10_3_merge_5utr_info_to_pclass_table.py \
--name Mot \
--utr_info mother/10_5p_utr/pb_5utr_categories.tsv \
--sqanti_protein_classification mother/09_sqanti_protein/Mot.sqanti_protein_classification.tsv \
--odir mother/10_5p_utr

conda deactivate
module purge
