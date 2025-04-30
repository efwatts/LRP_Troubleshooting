#!/bin/bash

#SBATCH --job-name=17_transcriptome_summary
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

module load gcc/11.4.0 openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda activate CDS_org

# Condition 1
gtfToGenePred 07_make_cds_gtf/HAEC/condition1_cds.gtf 17_track_visualization/HAEC/condition1.genePred
genePredToBed 17_track_visualization/HAEC/condition1.genePred 17_track_visualization/HAEC/condition1.bed12

python 00_scripts/17_rgb_by_cpm_to_bed.py --input_bed 17_track_visualization/HAEC/condition1.bed12 --day condition1 --output_file 17_track_visualization/HAEC/condition1.bed12

# Condition 2
gtfToGenePred 07_make_cds_gtf/HAEC/condition2_cds.gtf 17_track_visualization/HAEC/condition2.genePred
genePredToBed 17_track_visualization/HAEC/condition2.genePred 17_track_visualization/HAEC/condition2.bed12

python 00_scripts/17_rgb_by_cpm_to_bed.py --input_bed 17_track_visualization/HAEC/condition2.bed12 --day condition2 --output_file 17_track_visualization/HAEC/condition2.bed12

conda deactivate