#!/bin/bash

#SBATCH --job-name=05_orf-calling
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu
#SBATCH --mem=200G # memory per node 

# Load modules
module load apptainer/1.3.4
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

#activate conda env

conda activate orf-calling

# Command to open the container & run script
apptainer exec /project/sheynkman/dockers/LRP/orf_calling_latest.sif /bin/bash -c "\
    python 00_scripts/05_orf_calling_multisample.py \
    --orf_coord 04_CPAT/HAEC/HAEC.ORF_prob.tsv \
    --orf_fasta 04_CPAT/HAEC/HAEC.ORF_seqs.fa \
    --gencode /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
    --sample_gtf 03_filter_sqanti/HAEC/HAEC_corrected.5degfilter.gff \
    --pb_gene 04_transcriptome_summary/HAEC/pb_gene.tsv \
    --classification 03_filter_sqanti/HAEC/HAEC_classification.5degfilter.tsv \
    --sample_fasta 03_filter_sqanti/HAEC/HAEC_corrected.5degfilter.fasta \
    --output_mutant 05_orf_calling/HAEC/best_ORF_condition1.tsv \
    --output_wt 05_orf_calling/HAEC/best_ORF_condition2.tsv
"

conda deactivate
module purge