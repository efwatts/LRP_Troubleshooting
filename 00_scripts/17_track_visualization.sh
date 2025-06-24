#!/bin/bash

#SBATCH --job-name=17_transcriptome_summary
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=your_account_name #the account to charge the job to
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=your_email #your email address to receive notifications

module load gcc/11.4.0 openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda activate CDS_org

# make multiregion bed
python 00_scripts/17_make_multiregion_bed.py \
  --name MDS \
  --sample_gtf 07_make_cds_gtf/WT_cds.gtf \
  --reference_gtf /project/sheynkman/external_data/GENCODE_M35/gencode.vM35.basic.annotation.gtf

# Protein coding gene levels
# Condition 1 - Q157R
gtfToGenePred 07_make_cds_gtf/Q157R_cds.gtf 17_track_visualization/Q157R_protein.genePred
genePredToBed 17_track_visualization/Q157R.genePred 17_track_visualization/Q157R_protein.bed12

python 00_scripts/17_rgb_by_cpm_to_bed_PB.py --input_bed 17_track_visualization/Q157R_protein.bed12 --day condition2 --output_file 17_track_visualization/Q157R_protein.blue.bed12 --sqanti 03_filter_sqanti/MDS_classification.5degfilter.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/Q157R_protein.blue.bed12 --output_file 17_track_visualization/Q157R_protein.cpm.bed12 

# Condition 2 - WT
gtfToGenePred 07_make_cds_gtf/WT_cds.gtf 17_track_visualization/WT_protein.genePred
genePredToBed 17_track_visualization/WT.genePred 17_track_visualization/WT_protein.bed12

python 00_scripts/17_rgb_by_cpm_to_bed_PB.py --input_bed 17_track_visualization/WT_protein.bed12 --day condition1 --output_file 17_track_visualization/WT_protein.pink.bed12 --sqanti 03_filter_sqanti/MDS_classification.5degfilter.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/WT_protein.pink.bed12 --output_file 17_track_visualization/WT_protein.cpm.bed12


# Create a files that match the CPM from the edgeR analysis (because CPM is relative to the number of reads in the sample)
python 00_scripts/17_split_gtf_add_edgeR_cpm.py \
  -s 19_LRP_summary/protein/protein_isoform_DEG_summary_table.tsv \
  -g 03_filter_sqanti/MDS_corrected.5degfilter.gff \
  -m 17_track_visualization/Q157R.edgeR.protein.gtf \
  -w 17_track_visualization/WT.edgeR.protein.gtf

## Protein coding gene levels with edgeR CPMs
# Condition 1 - Q157R
gtfToGenePred 17_track_visualization/Q157R.edgeR.protein.gtf 17_track_visualization/Q157R_edgeR_protein.genePred
genePredToBed 17_track_visualization/Q157R_edgeR_protein.genePred 17_track_visualization/Q157R_edgeR_protein.bed12

python 00_scripts/17_rgb_by_cpm_to_bed_PB.py --input_bed 17_track_visualization/Q157R_edgeR_protein.bed12 --day condition2 --output_file 17_track_visualization/Q157R_edgeR_protein.blue.bed12 --sqanti 03_filter_sqanti/MDS_classification.5degfilter.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/Q157R_edgeR_protein.blue.bed12 --output_file 17_track_visualization/Q157R_edgeR_protein.cpm.bed12

# Condition 2 - WT
gtfToGenePred 17_track_visualization/WT.edgeR.protein.gtf 17_track_visualization/WT_edgeR_protein.genePred
genePredToBed 17_track_visualization/WT_edgeR_protein.genePred 17_track_visualization/WT_edgeR_protein.bed12

python 00_scripts/17_rgb_by_cpm_to_bed_PB.py --input_bed 17_track_visualization/WT_edgeR_protein.bed12 --day condition1 --output_file 17_track_visualization/WT_edgeR_protein.pink.bed12 --sqanti 03_filter_sqanti/MDS_classification.5degfilter.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/WT_edgeR_protein.pink.bed12 --output_file 17_track_visualization/WT_edgeR_protein.cpm.bed12

# Transcript isoform levels
# First, we need to split the SQANTI output into two files, one for Q157R and one for WT and calculate the CPMs for each transcript isoform
python 00_scripts/17_split_transcript_gtfs.py -i 03_filter_sqanti/MDS_classification.5degfilter.tsv -g 03_filter_sqanti/MDS_corrected.5degfilter.gff -p 04_transcriptome_summary/pb_gene.tsv -m 17_track_visualization/Q157R.filter_sqanti.gtf -w 17_track_visualization/WT.filter_sqanti.gtf

# Condition 1 - Q157R
gtfToGenePred 17_track_visualization/Q157R.filter_sqanti.gtf 17_track_visualization/Q157R_transcript.genePred
genePredToBed 17_track_visualization/Q157R_transcript.genePred 17_track_visualization/Q157R_transcript.bed12

python 00_scripts/17_rgb_by_cpm_to_bed_PB.py --input_bed 17_track_visualization/Q157R_transcript.bed12 --day condition2 --output_file 17_track_visualization/Q157R_transcript.blue.bed12 --sqanti 03_filter_sqanti/MDS_classification.5degfilter.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/Q157R_transcript.blue.bed12 --output_file 17_track_visualization/Q157R_transcript.cpm.bed12

# Condition 2 - WT
gtfToGenePred 17_track_visualization/WT.filter_sqanti.gtf 17_track_visualization/WT_transcript.genePred
genePredToBed 17_track_visualization/WT_transcript.genePred 17_track_visualization/WT_transcript.bed12

python 00_scripts/17_rgb_by_cpm_to_bed_PB.py --input_bed 17_track_visualization/WT_transcript.bed12 --day condition1 --output_file 17_track_visualization/WT_transcript.pink.bed12 --sqanti 03_filter_sqanti/MDS_classification.5degfilter.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/WT_transcript.pink.bed12 --output_file 17_track_visualization/WT_transcript.cpm.bed12

# Create a files that match the CPM from the edgeR analysis (because CPM is relative to the number of reads in the sample)
# First, split the SQANTI output into two files, one for Q157R and one for WT with the CPMs from the edgeR analysis
python 00_scripts/17_split_gtf_add_edgeR_cpm.py \
  -s 19_LRP_summary/transcript_DEG_summary_table.tsv \
  -g 03_filter_sqanti/MDS_corrected.5degfilter.gff \
  -m 17_track_visualization/Q157R.edgeR.gtf \
  -w 17_track_visualization/WT.edgeR.gtf

## Transcript isoform levels with edgeR CPMs
# Condition 1 - Q157R
gtfToGenePred 17_track_visualization/Q157R.edgeR.gtf 17_track_visualization/Q157R_edgeR_transcript.genePred
genePredToBed 17_track_visualization/Q157R_edgeR_transcript.genePred 17_track_visualization/Q157R_edgeR_transcript.bed12

python 00_scripts/17_rgb_by_cpm_to_bed_PB.py --input_bed 17_track_visualization/Q157R_edgeR_transcript.bed12 --day condition2 --output_file 17_track_visualization/Q157R_edgeR_transcript.blue.bed12 --sqanti 03_filter_sqanti/MDS_classification.5degfilter.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/Q157R_edgeR_transcript.blue.bed12 --output_file 17_track_visualization/Q157R_edgeR_transcript.cpm.bed12

# Condition 2 - WT
gtfToGenePred 17_track_visualization/WT.edgeR.gtf 17_track_visualization/WT_edgeR_transcript.genePred
genePredToBed 17_track_visualization/WT_edgeR_transcript.genePred 17_track_visualization/WT_edgeR_transcript.bed12

python 00_scripts/17_rgb_by_cpm_to_bed_PB.py --input_bed 17_track_visualization/WT_edgeR_transcript.bed12 --day condition1 --output_file 17_track_visualization/WT_edgeR_transcript.pink.bed12 --sqanti 03_filter_sqanti/MDS_classification.5degfilter.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/WT_edgeR_transcript.pink.bed12 --output_file 17_track_visualization/WT_edgeR_transcript.cpm.bed12

conda deactivate