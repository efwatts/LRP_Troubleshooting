#!/bin/bash

#SBATCH --job-name=07_cds_gtf
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

# Load modules
module load apptainer/1.2.2
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load miniforge/24.3.0-py3.11

#activate conda env
source $(conda info --base)/etc/profile.d/conda.sh

conda activate reference_tab

# Command to open the container & run script

apptainer exec pb-cds-gtf_latest.sif /bin/bash -c " \
    python ./00_scripts/07_make_pacbio_cds_gtf.py \
    --sample_gtf ./03_filter_sqanti/filtered_jurkat_corrected.gtf \
    --agg_orfs ./06_refine_orf_database/jurkat_30_orf_refined.tsv \
    --refined_orfs ./05_orf_calling/jurkat_best_ORF.tsv \
    --pb_gene ./04_transcriptome_summary/pb_gene.tsv \
    --output_cds ./07_make_cds_gtf/jurkat_cds.gtf
"

exit
conda deactivate
module purge
