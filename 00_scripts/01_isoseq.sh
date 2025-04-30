#!/bin/bash

#SBATCH --job-name=01_isoseq
#SBATCH --cpus-per-task=10          
#SBATCH --nodes=1                   
#SBATCH --ntasks-per-node=1         
#SBATCH --mem=1460G           
#SBATCH --time=72:00:00             
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab_paid
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

module load isoseqenv/py3.7
module load gcc/11.4.0
module load bedops/2.4.41
module load nseg/1.0.0
module load bioconda/py3.10
module load smrtlink/13.1.0.221970
module load miniforge/24.3.0-py3.11

pbmerge -o 01_isoseq/merge/merged.flnc.bam /project/sheynkman/raw_data/PacBio/Sample-1-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-2-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-3-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-4-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-5-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-6-flnc.bam

# Cluster reads
isoseq cluster2 01_isoseq/merge/merged.flnc.bam 01_isoseq/cluster/merged.clustered.bam

# Align reads to the genome 
pbmm2 align /project/sheynkman/external_data/GENCODE_v47/GRCh38.primary_assembly.genome.fa 01_isoseq/cluster/merged.clustered.bam 01_isoseq/align/merged.aligned.bam --preset ISOSEQ --sort -j 40 --log-level INFO

# Collapse redundant reads
isoseq collapse --do-not-collapse-extra-5exons 01_isoseq/align/merged.aligned.bam 01_isoseq/merge/merged.flnc.bam 01_isoseq/collapse/merged.collapsed.gff

conda deactivate
module purge
