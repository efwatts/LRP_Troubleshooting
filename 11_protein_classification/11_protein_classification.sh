#!/bin/bash

#SBATCH --job-name=protein_classification
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

conda activate protein_class

# Mother
python ./00_scripts/11_protein_classification_add_meta.py \
--protein_classification  mother/10_5p_utr/Mot.sqanti_protein_classification_w_5utr_info.tsv \
--best_orf mother/05_orf_calling/Mot_best_ORF.tsv \
--refined_meta mother/06_refine_orf_database/Mot_30_orf_refined.tsv \
--ensg_gene ./01_reference_tables/ensg_gene.tsv \
--name Mot \
--dest_dir mother/11_protein_classification/


python ./00_scripts/11_protein_classification.py \
--sqanti_protein mother/11_protein_classification/Mot.protein_classification_w_meta.tsv \
--name Mot \
--dest_dir mother/11_protein_classification/

conda deactivate
module purge
