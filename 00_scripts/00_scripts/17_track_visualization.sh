#!/bin/bash

#SBATCH --job-name=17_transcriptome_summary
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab_paid
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

module load gcc/11.4.0 openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11
module load bedtools

conda activate CDS_org

#########################################################################
######################## Multiregion BED File ###########################
#########################################################################

# make multiregion bed
python 00_scripts/17_make_multiregion_bed.py \
  --name MDS \
  --sample_gtf 07_make_cds_gtf/WT_cds.gtf \
  --reference_gtf /project/sheynkman/external_data/GENCODE_M35/gencode.vM35.basic.annotation.gtf

#########################################################################
########################## Transcript Level #############################
#########################################################################
# Transcript isoform levels - full filtered SQANTI output
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

#########################################################################
############################ Protein Level ##############################
#########################################################################
# Refined ORF database - from 07_make_cds_gtf
# Condition 1 - Q157R
gtfToGenePred 07_make_cds_gtf/Q157R_cds.gtf 17_track_visualization/Q157R_refined_protein.genePred
genePredToBed 17_track_visualization/Q157R_refined_protein.genePred 17_track_visualization/Q157R_refined_protein.bed12
python 00_scripts/17_rgb_by_cpm_to_bed_PB_protein.py --input_bed 17_track_visualization/Q157R_refined_protein.bed12 --day condition2 --output_file 17_track_visualization/Q157R_refined_protein.blue.bed12 --sqanti 09_sqanti_protein/Q157R.sqanti_protein_classification.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/Q157R_refined_protein.blue.bed12 --output_file 17_track_visualization/Q157R_refined_protein.cpm.bed12
# Condition 2 - WT
gtfToGenePred 07_make_cds_gtf/WT_cds.gtf 17_track_visualization/WT_refined_protein.genePred
genePredToBed 17_track_visualization/WT_refined_protein.genePred 17_track_visualization/WT_refined_protein.bed12
python 00_scripts/17_rgb_by_cpm_to_bed_PB_protein.py --input_bed 17_track_visualization/WT_refined_protein.bed12 --day condition1 --output_file 17_track_visualization/WT_refined_protein.pink.bed12 --sqanti 09_sqanti_protein/WT.sqanti_protein_classification.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/WT_refined_protein.pink.bed12 --output_file 17_track_visualization/WT_refined_protein.cpm.bed12

# Filtered protein database - from 13_protein_filter
# Condition 1 - Q157R
gtfToGenePred 13_protein_filter/Q157R_with_cds_filtered.gtf 17_track_visualization/Q157R_filtered_protein.genePred
genePredToBed 17_track_visualization/Q157R_filtered_protein.genePred 17_track_visualization/Q157R_filtered_protein.bed12
python 00_scripts/17_rgb_by_cpm_to_bed_PB_protein_filtered.py --input_bed 17_track_visualization/Q157R_filtered_protein.bed12 --day condition2 --output_file 17_track_visualization/Q157R_filtered_protein.blue.bed12
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/Q157R_filtered_protein.blue.bed12 --output_file 17_track_visualization/Q157R_filtered_protein.cpm.bed12
# Condition 2 - WT
gtfToGenePred 13_protein_filter/WT_with_cds_filtered.gtf 17_track_visualization/WT_filtered_protein.genePred
genePredToBed 17_track_visualization/WT_filtered_protein.genePred 17_track_visualization/WT_filtered_protein.bed12
python 00_scripts/17_rgb_by_cpm_to_bed_PB_protein_filtered.py --input_bed 17_track_visualization/WT_filtered_protein.bed12 --day condition1 --output_file 17_track_visualization/WT_filtered_protein.pink.bed12
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/WT_filtered_protein.pink.bed12 --output_file 17_track_visualization/WT_filtered_protein.cpm.bed12


# Create files that match the CPM from the edgeR analysis (because CPM is relative to the number of reads in the sample)
# Use filtered protein database - from 13_protein_filter
python 00_scripts/17_filter_DE_proteins.py \
  -i 19_LRP_summary/protein/protein_isoform_DEG_summary_table.tsv \
  --gtf_q157r 13_protein_filter/Q157R_with_cds_filtered.gtf \
  --gtf_wt 13_protein_filter/WT_with_cds_filtered.gtf \
  -m 17_track_visualization/Q157R.edgeR.protein.gtf \
  -w 17_track_visualization/WT.edgeR.protein.gtf

## Protein coding gene levels with edgeR CPMs
# Condition 1 - Q157R
gtfToGenePred 17_track_visualization/Q157R.edgeR.protein.gtf 17_track_visualization/Q157R_edgeR_filtered_protein.genePred
genePredToBed 17_track_visualization/Q157R_edgeR_filtered_protein.genePred 17_track_visualization/Q157R_edgeR_filtered_protein.bed12
python 00_scripts/17_rgb_by_cpm_to_bed_PB_protein.py --input_bed 17_track_visualization/Q157R_edgeR_filtered_protein.bed12 --day condition2 --output_file 17_track_visualization/Q157R_edgeR_filtered_protein.blue.bed12 --sqanti 09_sqanti_protein/Q157R.sqanti_protein_classification.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/Q157R_edgeR_filtered_protein.blue.bed12 --output_file 17_track_visualization/Q157R_edgeR_filtered_protein.cpm.bed12

# Condition 2 - WT
gtfToGenePred 17_track_visualization/WT.edgeR.protein.gtf 17_track_visualization/WT_edgeR_filtered_protein.genePred
genePredToBed 17_track_visualization/WT_edgeR_filtered_protein.genePred 17_track_visualization/WT_edgeR_filtered_protein.bed12
python 00_scripts/17_rgb_by_cpm_to_bed_PB_protein.py --input_bed 17_track_visualization/WT_edgeR_filtered_protein.bed12 --day condition1 --output_file 17_track_visualization/WT_edgeR_filtered_protein.pink.bed12 --sqanti 09_sqanti_protein/WT.sqanti_protein_classification.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/WT_edgeR_filtered_protein.pink.bed12 --output_file 17_track_visualization/WT_edgeR_filtered_protein.cpm.bed12


#########################################################################
################### Alternative Splicing Events ##########################
#########################################################################
# Skipping exon (SE) events
# First, remove the first line from the GTF file, which is a comment line
grep -v "^track" 18_SUPPA/01_splice_events/all.events_SE_strict.gtf > 18_SUPPA/01_splice_events/SE_events.cleaned.gtf
# Then, convert the cleaned GTF file to genePred format and then to BED12 format
gtfToGenePred 18_SUPPA/01_splice_events/SE_events.cleaned.gtf 17_track_visualization/SE_events.genePred
genePredToBed 17_track_visualization/SE_events.genePred 17_track_visualization/SE_events.bed12
# color-code the BED12 file based on the PSI values
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/SE_events.bed12 \
  --psi_summary 19_LRP_summary/alternative_splice_summary.tsv \
  --event_type SE \
  --output_prefix 17_track_visualization/SE_colored \
  --psi_column_wt avg_PSI_WT \
  --psi_column_mutant avg_PSI_Q157R

# Mutually exclusive exons (MX) events
# First, remove the first line from the GTF file, which is a comment line
grep -v "^track" 18_SUPPA/01_splice_events/all.events_MX_strict.gtf > 18_SUPPA/01_splice_events/MX_events.cleaned.gtf
# Then, convert the cleaned GTF file to genePred format and then to BED12 format
gtfToGenePred 18_SUPPA/01_splice_events/MX_events.cleaned.gtf 17_track_visualization/MX_events.genePred
genePredToBed 17_track_visualization/MX_events.genePred 17_track_visualization/MX_events.bed12
# color-code the BED12 file based on the PSI values 
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/MX_events.bed12 \
  --psi_summary 19_LRP_summary/alternative_splice_summary.tsv \
  --event_type MX \
  --output_prefix 17_track_visualization/MX_colored \
  --psi_column_wt avg_PSI_WT \
  --psi_column_mutant avg_PSI_Q157R

# Alternative 5' splice site (A5) events
# First, remove the first line from the GTF file, which is a comment line
grep -v "^track" 18_SUPPA/01_splice_events/all.events_A5_strict.gtf > 18_SUPPA/01_splice_events/A5_events.cleaned.gtf
# Then, convert the cleaned GTF file to genePred format and then to BED12 format
gtfToGenePred 18_SUPPA/01_splice_events/A5_events.cleaned.gtf 17_track_visualization/A5_events.genePred
genePredToBed 17_track_visualization/A5_events.genePred 17_track_visualization/A5_events.bed12
# color-code the BED12 file based on the PSI values 
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/A5_events.bed12 \
  --psi_summary 19_LRP_summary/alternative_splice_summary.tsv \
  --event_type A5 \
  --output_prefix 17_track_visualization/A5_colored \
  --psi_column_wt avg_PSI_WT \
  --psi_column_mutant avg_PSI_Q157R

# Alternative 3' splice site (A3) events
# First, remove the first line from the GTF file, which is a comment line
grep -v "^track" 18_SUPPA/01_splice_events/all.events_A3_strict.gtf > 18_SUPPA/01_splice_events/A3_events.cleaned.gtf
# Then, convert the cleaned GTF file to genePred format and then to BED12 format
gtfToGenePred 18_SUPPA/01_splice_events/A3_events.cleaned.gtf 17_track_visualization/A3_events.genePred
genePredToBed 17_track_visualization/A3_events.genePred 17_track_visualization/A3_events.bed12
# color-code the BED12 file based on the PSI values
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/A3_events.bed12 \
  --psi_summary 19_LRP_summary/alternative_splice_summary.tsv \
  --event_type A3 \
  --output_prefix 17_track_visualization/A3_colored \
  --psi_column_wt avg_PSI_WT \
  --psi_column_mutant avg_PSI_Q157R

# Retained intron (RI) events
# First, remove the first line from the GTF file, which is a comment line
grep -v "^track" 18_SUPPA/01_splice_events/all.events_RI_strict.gtf > 18_SUPPA/01_splice_events/RI_events.cleaned.gtf
# Then, convert the cleaned GTF file to genePred format and then to BED12 format
gtfToGenePred 18_SUPPA/01_splice_events/RI_events.cleaned.gtf 17_track_visualization/RI_events.genePred
genePredToBed 17_track_visualization/RI_events.genePred 17_track_visualization/RI_events.bed12
# color-code the BED12 file based on the PSI values
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/RI_events.bed12 \
  --psi_summary 19_LRP_summary/alternative_splice_summary.tsv \
  --event_type RI \
  --output_prefix 17_track_visualization/RI_colored \
  --psi_column_wt avg_PSI_WT \
  --psi_column_mutant avg_PSI_Q157R

# Alternative first exon (AF) events
# First, remove the first line from the GTF file, which is a comment line
grep -v "^track" 18_SUPPA/01_splice_events/all.events_AF_strict.gtf > 18_SUPPA/01_splice_events/AF_events.cleaned.gtf
# Then, convert the cleaned GTF file to genePred format and then to BED12 format
gtfToGenePred 18_SUPPA/01_splice_events/AF_events.cleaned.gtf 17_track_visualization/AF_events.genePred
genePredToBed 17_track_visualization/AF_events.genePred 17_track_visualization/AF_events.bed12
# color-code the BED12 file based on the PSI values
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/AF_events.bed12 \
  --psi_summary 19_LRP_summary/alternative_splice_summary.tsv \
  --event_type AF \
  --output_prefix 17_track_visualization/AF_colored \
  --psi_column_wt avg_PSI_WT \
  --psi_column_mutant avg_PSI_Q157R

# Alternative last exon (AL) events
# First, remove the first line from the GTF file, which is a comment line
grep -v "^track" 18_SUPPA/01_splice_events/all.events_AL_strict.gtf > 18_SUPPA/01_splice_events/AL_events.cleaned.gtf
# Then, convert the cleaned GTF file to genePred format and then to BED12 format
gtfToGenePred 18_SUPPA/01_splice_events/AL_events.cleaned.gtf 17_track_visualization/AL_events.genePred
genePredToBed 17_track_visualization/AL_events.genePred 17_track_visualization/AL_events.bed12
# color-code the BED12 file based on the PSI values 
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/AL_events.bed12 \
  --psi_summary 19_LRP_summary/alternative_splice_summary.tsv \
  --event_type AL \
  --output_prefix 17_track_visualization/AL_colored \
  --psi_column_wt avg_PSI_WT \
  --psi_column_mutant avg_PSI_Q157R

conda deactivate