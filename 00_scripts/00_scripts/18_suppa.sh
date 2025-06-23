#!/bin/bash

#SBATCH --job-name=18_suppa
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=24:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

module load gcc
module load openmpi
module load python
module load miniforge
module load R

module load gcc/12.4.0

conda activate suppa

#Generate splicing events. 
python /project/sheynkman/programs/SUPPA-2.4/suppa.py generateEvents \
    -i 03_filter_sqanti/MDS_corrected.5degfilter.gff \
    -o 18_SUPPA/01_splice_events/all.events \
    -e SE SS MX RI FL -f ioe

#Put all IOE events in the same file.
# this step occasionally runs for hours and makes massive files, so it is best to check on it
cd 18_SUPPA/01_splice_events

awk '
    FNR==1 && NR!=1 { while (/^<header>/) getline; }
    1 {print}
' *.ioe > all.events.ioe

cd ../..

#Create expression table.
python 00_scripts/18_expression_table.py \
  03_filter_sqanti/MDS_classification.5degfilter.tsv \
  18_SUPPA/expression_table_cpm.tsv

#Calculate PSI values.
python /project/sheynkman/programs/SUPPA-2.4/suppa.py psiPerEvent \
  --ioe-file 18_SUPPA/01_splice_events/all.events.ioe \
  --expression-file 18_SUPPA/expression_table_cpm.tsv \
  -o 18_SUPPA/combined_local


#Differential splicing. Split the PSI and TPM files between the two conditions (if comparing)
Rscript 00_scripts/18_suppa_split_file.R \
  18_SUPPA/expression_table_cpm.tsv \
  BioSample_1,BioSample_3,BioSample_4 \
  BioSample_2,BioSample_5,BioSample_6 \
  18_SUPPA/WT.tpm \
  18_SUPPA/Q157R.tpm -i

Rscript 00_scripts/18_suppa_split_file.R \
  18_SUPPA/combined_local.psi \
  BioSample_1,BioSample_3,BioSample_4 \
  BioSample_2,BioSample_5,BioSample_6 \
  18_SUPPA/WT.psi \
  18_SUPPA/Q157R.psi -e

#Analyze differential splicing.
python /project/sheynkman/programs/SUPPA-2.4/suppa.py diffSplice \
  --method empirical \
  --input 18_SUPPA/01_splice_events/all.events.ioe \
  --psi 18_SUPPA/WT.psi 18_SUPPA/Q157R.psi \
  --tpm 18_SUPPA/WT.tpm 18_SUPPA/Q157R.tpm \
  --gene-correction \
  --lower-bound 0.05 \
  --save_tpm_events \
  --nan-threshold 0.33 \
  --output 18_SUPPA/MDS_diffsplice

conda deactivate
module purge