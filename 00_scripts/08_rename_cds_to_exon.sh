#!/bin/bash

#SBATCH --job-name=08_rename_cds_to_exon
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

conda activate reference_tab

apptainer exec /project/sheynkman/dockers/LRP/pb-cds-gtf_latest.sif /bin/bash -c " \
  python 00_scripts/08_rename_cds_to_exon_multi.py \
  --sample1_gtf 07_make_cds_gtf/condition1_cds.gtf \
  --sample1_name 08_rename_cds_to_exon/condition1 \
  --sample2_gtf 07_make_cds_gtf/condition2_cds.gtf \
  --sample2_name 08_rename_cds_to_exon/condition2 \
  --reference_gtf /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
  --reference_name 08_rename_cds_to_exon/gencode \
  --num_cores 8 
"

conda deactivate 
module purge