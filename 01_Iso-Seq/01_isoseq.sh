#!/bin/bash

#SBATCH --job-name=isoseq3
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

module load isoseqenv/py3.7
module load apptainer/1.2.2
module load gcc/11.4.0
module load bedops/2.4.41
module load mamba/22.11.1-4
module load nseg/1.0.0
module load bioconda/py3.10
module load anaconda/2023.07-py3.11
module load smrtlink/12.0.0.177059


# Change to the working directory
cd /project/sheynkman/users/emily/LRP_test/jurkat

conda activate isoseq_env

pbindex ./00_input_data/jurkat_merged.ccs.bam

bamtools filter -tag 'rq':'>=0.90' -in ./00_input_data/jurkat_merged.ccs.bam -out ./01_isoseq/filter/filtered.merged.bam

# Find and remove adapters/barcodes
lima --isoseq --dump-clips --peek-guess -j 4 ./01_isoseq/filter/filtered.merged.bam ./00_input_data/NEB_primers.fasta ./01_isoseq/lima/merged.demult.bam

# Filter for non-concatamer, polyA-containing reads
isoseq3 refine --require-polya ./01_isoseq/lima/merged.demult.NEB_5p--NEB_3p.bam ./00_input_data/NEB_primers.fasta ./01_isoseq/refine/merged.flnc.bam

# Cluster reads
isoseq3 cluster ./01_isoseq/refine/merged.flnc.bam ./01_isoseq/cluster/merged.clustered.bam --verbose --use-qvs

# Align reads to the genome 
pbmm2 align ./00_input_data/GRCh38.primary_assembly.genome.fa ./01_isoseq/cluster/merged.clustered.hq.bam ./01_isoseq/align/merged.aligned.bam --preset ISOSEQ --sort -j 40 --log-level INFO

# Collapse redundant reads
isoseq3 collapse ./01_isoseq/align/merged.aligned.bam ./01_isoseq/collapse/merged.collapsed.gff

conda deactivate
