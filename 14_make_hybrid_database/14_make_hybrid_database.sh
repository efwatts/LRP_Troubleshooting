#!/bin/bash

#SBATCH --job-name=make_hybrid_database
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
python ./00_scripts/14_make_hybrid_database.py \
    --protein_classification mother/13_protein_filter/Mot.classification_filtered.tsv \
    --gene_lens ./01_reference_tables/gene_lens.tsv \
    --pb_fasta mother/13_protein_filter/Mot.filtered_protein.fasta \
    --gc_fasta ./02_make_gencode_database/gencode_clusters.fasta \
    --refined_info mother/12_protein_gene_rename/Mot_orf_refined_gene_update.tsv \
    --pb_cds_gtf mother/13_protein_filter/Mot_with_cds_filtered.gtf \
    --name mother/14_protein_hybrid_database/Mot

conda deactivate
module purge
