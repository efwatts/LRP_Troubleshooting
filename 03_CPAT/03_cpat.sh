#!/bin/bash

#SBATCH --job-name=cpat
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

# Load necessary modules (if needed)
module purge
module load gcc/11.4.0
module load openmpi/4.1.4
module load python/3.11.4

cd /project/sheynkman/users/emily/LRP_test/jurkat

   -x ./00_input_data/Human_Hexamer.tsv \
   -d H./00_input_data/uman_logitModel.RData \
   -g ./02_sqanti/output/jurkat_corrected.fasta \
   --min-orf=50 \
   --top-orf=50 \
   -o ./03_CPAT/cpat_out \
   2> cpat.error
