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


module load isoseqenv
module load gcc
module load bedops
module load nseg
module load bioconda
module load smrtlink
module load miniforge
module load samtools

mkdir 01_isoseq/cluster
mkdir 01_isoseq/align
mkdir 01_isoseq/collapse
mkdir 01_isoseq/merge

pbmerge -o 01_isoseq/merge/merged.flnc.bam /project/sheynkman/raw_data/PacBio/Sample-1-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-2-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-3-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-4-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-5-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-6-flnc.bam

# Cluster reads
isoseq cluster2 01_isoseq/merge/merged.flnc.bam 01_isoseq/cluster/merged.clustered.bam

# Align reads to the genome 
pbmm2 align /project/sheynkman/external_data/GENCODE_v47/GRCh38.primary_assembly.genome.fa 01_isoseq/cluster/merged.clustered.bam 01_isoseq/align/merged.aligned.bam --preset ISOSEQ --sort -j 40 --log-level INFO

# Collapse redundant reads
# Default: max fuzzy junctions 5, max 5p diff 50 max 3p diff 100
isoseq collapse --max-fuzzy-junction 0 --max-5p-diff 100 --max-3p-diff 200 01_isoseq/align/merged.aligned.bam 01_isoseq/merge/merged.flnc.bam 01_isoseq/collapse/merged.collapsed.gff

conda deactivate
module purge
