#!/bin/bash

#SBATCH --job-name=protein_gene_rename
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
module load miniforge/24.3.0-py3.11

source $(conda info --base)/etc/profile.d/conda.sh
conda activate protein_class

# Mother
python ./00_scripts/12_protein_gene_rename.py \
    --sample_gtf mother/07_make_cds_gtf/Mot_with_cds.gtf \
    --sample_protein_fasta mother/06_refine_orf_database/Mot_orf_refined.fasta \
    --sample_refined_info mother/06_refine_orf_database/Mot_orf_refined.tsv \
    --pb_protein_genes mother/11_protein_classification/Mot_genes.tsv \
    --name mother/12_protein_gene_rename/Mot

conda deactivate
module purge
