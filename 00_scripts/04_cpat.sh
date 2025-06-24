#!/bin/bash

#SBATCH --job-name=04_cpat
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=1:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=your_account_name #the account to charge the job to
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=your_email #your email address to receive notifications

# Load necessary modules (if needed)
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load R/4.3.1
module load miniforge/24.3.0-py3.11

export PATH="$HOME/.local/bin:$PATH"

cpat \
   -x /project/sheynkman/external_data/CPAT_data/Human_Hexamer.tsv \
   -d /project/sheynkman/external_data/CPAT_data/Human_logitModel.RData \
   -g 03_filter_sqanti/sample_corrected.5degfilter.fasta \
   --min-orf=50 \
   --top-orf=50 \
   -o 04_CPAT/sample \
   2> 04_CPAT/sample_cpat.error

python 00_scripts/04_filter_cpat_results.py \
  --cpat_output 04_CPAT/sample.ORF_prob.tsv \
  --input_fasta 03_filter_sqanti/sample_corrected.5degfilter.fasta \
  --output_dir 04_CPAT/dropout \
  --prefix sample

conda deactivate
module purge

