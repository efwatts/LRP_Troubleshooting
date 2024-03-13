#!/bin/bash
#SBATCH --job-name=isoseqSQANTI_toytest
#SBATCH -A sheynkman_lab
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=10
#SBATCH --time=1:00:00
#SBATCH -p dev #the queue/partition to run on

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

mkdir ./filter/
mkdir ./lima/
mkdir ./refine/
mkdir ./cluster/
mkdir ./align/
mkdir ./collapse/


# Change to the working directory
cd /scratch/yqy3cu/LRP_tutorial/IsoSeqSQANTI/toy

conda activate isoseq_testenv

# Ensure that only qv10 reads from ccs are input 
bamtools filter -tag 'rq':'>=0.90' -in data/jurkat.codethon_toy.ccs.bam -out filter/filtered.merged.bam

# Find and remove adapters/barcodes
lima --isoseq --dump-clips --peek-guess -j 4 filter/filtered.merged.bam data/NEB_primers.fasta lima/merged.demult.bam

# Filter for non-concatamer, polyA-containing reads
isoseq3 refine --require-polya lima/merged.demult.NEB_5p--NEB_3p.bam data/NEB_primers.fasta refine/merged.flnc.bam

# Cluster reads
isoseq3 cluster refine/merged.flnc.bam cluster/merged.clustered.bam --verbose --use-qvs

# Align reads to the genome 
pbmm2 align data/GRCh38.primary_assembly.genome.chr22.fa cluster/merged.clustered.hq.bam align/merged.aligned.bam --preset ISOSEQ --sort -j 40 --log-level INFO

# Collapse redundant reads
isoseq3 collapse align/merged.aligned.bam collapse/merged.collapsed.gff

conda deactivate
