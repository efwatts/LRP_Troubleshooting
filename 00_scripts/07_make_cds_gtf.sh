#!/bin/bash

#SBATCH --job-name=07_cds_gtf
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=your_account_name #the account to charge the job to
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=your_email #your email address to receive notifications

# Load modules
module load apptainer
module load gcc
module load openmpi
module load python
module load miniforge

source $(conda info --base)/etc/profile.d/conda.sh

#activate conda env

conda activate reference_tab

# condition1
# Command to open the container & run script

apptainer exec /project/sheynkman/dockers/LRP/pb-cds-gtf_latest.sif /bin/bash -c " \
    python 00_scripts/07_make_pacbio_cds_gtf.py \
    --sample_gtf 03_filter_sqanti/sample_corrected.5degfilter.gff \
    --agg_orfs 06_refine_orf_database/condition1_0_orf_refined.tsv \
    --refined_orfs 05_orf_calling/best_ORF_condition1.tsv \
    --pb_gene 04_transcriptome_summary/pb_gene.tsv \
    --output_cds 07_make_cds_gtf/condition1_cds.gtf
"

# condition2
# Command to open the container & run script

apptainer exec /project/sheynkman/dockers/LRP/pb-cds-gtf_latest.sif /bin/bash -c " \
    python 00_scripts/07_make_pacbio_cds_gtf.py \
    --sample_gtf 03_filter_sqanti/sample_corrected.5degfilter.gff \
    --agg_orfs 06_refine_orf_database/condition2_0_orf_refined.tsv \
    --refined_orfs 05_orf_calling/best_ORF_condition2.tsv \
    --pb_gene 04_transcriptome_summary/pb_gene.tsv \
    --output_cds 07_make_cds_gtf/condition2_cds.gtf
"

conda deactivate
module purge