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
module load bioconda/py3.10
module load bedtools

conda activate CDS_org

##########################################################################
########################## Transcript Level #############################
#########################################################################
# Create a files that match the CPM from the edgeR analysis (because CPM is relative to the number of reads in the sample)
# First, split the SQANTI output into two files, one for SRSF2_WT and one for NBM with the CPMs from the edgeR analysis
python 00_scripts/17_split_gtf_add_edgeR_cpm.py \
  -s 19_LRP_summary/edgeR/edgeR_transcript/transcript_DEG_summary_table_SRSF2WTvsNBM.tsv \
  -g /project/sheynkman/projects/LRP_AML/03_filter_sqanti/AML_corrected.5degfilter.gff \
  -o 17_track_visualization \
  -p AML

## Transcript isoform levels with edgeR CPMs
# Condition 1 - SRSF2WT
gtfToGenePred 17_track_visualization/AML_SRSF2WT.gtf 17_track_visualization/SRSF2WT_edgeR_transcript.genePred
genePredToBed 17_track_visualization/SRSF2WT_edgeR_transcript.genePred 17_track_visualization/SRSF2WT_edgeR_transcript.bed12
python 00_scripts/17_rgb_by_cpm_to_bed_PB.py --input_bed 17_track_visualization/SRSF2WT_edgeR_transcript.bed12 --day condition2 --output_file 17_track_visualization/SRSF2WT_edgeR_transcript.blue.bed12 --sqanti /project/sheynkman/projects/LRP_AML/03_filter_sqanti/AML_classification.5degfilter.tsv
python 00_scripts/17_cpm_blackred.py --input_bed 17_track_visualization/SRSF2WT_edgeR_transcript.blue.bed12 --output_file 17_track_visualization/SRSF2WT_edgeR_transcript.cpm.bed12

# Condition 2 - NBM
gtfToGenePred 17_track_visualization/AML_NBM.gtf 17_track_visualization/NBM_edgeR_transcript.genePred
genePredToBed 17_track_visualization/NBM_edgeR_transcript.genePred 17_track_visualization/NBM_edgeR_transcript.bed12
python 00_scripts/17_rgb_by_cpm_to_bed_PB.py --input_bed 17_track_visualization/NBM_edgeR_transcript.bed12 --day condition1 --output_file 17_track_visualization/NBM_edgeR_transcript.pink.bed12 --sqanti /project/sheynkman/projects/LRP_AML/03_filter_sqanti/AML_classification.5degfilter.tsv
python 00_scripts/17_cpm_blackred.py --input_bed 17_track_visualization/NBM_edgeR_transcript.pink.bed12 --output_file 17_track_visualization/NBM_edgeR_transcript.cpm.bed12

#########################################################################
############# SUPPA Alternative Splicing Events #########################
#########################################################################

# SUPPA events
# SE events
grep -v "^track" /project/sheynkman/projects/LRP_AML/allAMLvNBM/18_SUPPA/01_splice_events/all.events_SE_strict.gtf > 18_SUPPA/01_splice_events/SE_events.cleaned.gtf
gtfToGenePred 18_SUPPA/01_splice_events/SE_events.cleaned.gtf 17_track_visualization/SE_events.genePred
genePredToBed 17_track_visualization/SE_events.genePred 17_track_visualization/SE_events.bed12
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/SE_events.bed12 \
  --psi_summary 19_LRP_summary/SRSF2WTvNBM_alternative_splice_summary.tsv \
  --event_type SE \
  --output_prefix 17_track_visualization/suppa_tracks/SE_colored \
  --psi_column_NBM avg_PSI_NBM \
  --psi_column_mutant avg_PSI_SRSF2WT

# MX events
grep -v "^track" /project/sheynkman/projects/LRP_AML/allAMLvNBM/18_SUPPA/01_splice_events/all.events_MX_strict.gtf > 18_SUPPA/01_splice_events/MX_events.cleaned.gtf
gtfToGenePred 18_SUPPA/01_splice_events/MX_events.cleaned.gtf 17_track_visualization/MX_events.genePred
genePredToBed 17_track_visualization/MX_events.genePred 17_track_visualization/MX_events.bed12
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/MX_events.bed12 \
  --psi_summary 19_LRP_summary/SRSF2WTvNBM_alternative_splice_summary.tsv \
  --event_type MX \
  --output_prefix 17_track_visualization/suppa_tracks/MX_colored \
  --psi_column_NBM avg_PSI_NBM \
  --psi_column_mutant avg_PSI_SRSF2WT

# A5 events
grep -v "^track" /project/sheynkman/projects/LRP_AML/allAMLvNBM/18_SUPPA/01_splice_events/all.events_A5_strict.gtf > 18_SUPPA/01_splice_events/A5_events.cleaned.gtf
gtfToGenePred 18_SUPPA/01_splice_events/A5_events.cleaned.gtf 17_track_visualization/A5_events.genePred
genePredToBed 17_track_visualization/A5_events.genePred 17_track_visualization/A5_events.bed12
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/A5_events.bed12 \
  --psi_summary 19_LRP_summary/SRSF2WTvNBM_alternative_splice_summary.tsv \
  --event_type A5 \
  --output_prefix 17_track_visualization/suppa_tracks/A5_colored \
  --psi_column_NBM avg_PSI_NBM \
  --psi_column_mutant avg_PSI_SRSF2WT

# A3 events
grep -v "^track" /project/sheynkman/projects/LRP_AML/allAMLvNBM/18_SUPPA/01_splice_events/all.events_A3_strict.gtf > 18_SUPPA/01_splice_events/A3_events.cleaned.gtf
gtfToGenePred 18_SUPPA/01_splice_events/A3_events.cleaned.gtf 17_track_visualization/A3_events.genePred
genePredToBed 17_track_visualization/A3_events.genePred 17_track_visualization/A3_events.bed12
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/A3_events.bed12 \
  --psi_summary 19_LRP_summary/SRSF2WTvNBM_alternative_splice_summary.tsv \
  --event_type A3 \
  --output_prefix 17_track_visualization/suppa_tracks/A3_colored \
  --psi_column_NBM avg_PSI_NBM \
  --psi_column_mutant avg_PSI_SRSF2WT

# RI events
grep -v "^track" /project/sheynkman/projects/LRP_AML/allAMLvNBM/18_SUPPA/01_splice_events/all.events_RI_strict.gtf > 18_SUPPA/01_splice_events/RI_events.cleaned.gtf
gtfToGenePred 18_SUPPA/01_splice_events/RI_events.cleaned.gtf 17_track_visualization/RI_events.genePred
genePredToBed 17_track_visualization/RI_events.genePred 17_track_visualization/RI_events.bed12
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/RI_events.bed12 \
  --psi_summary 19_LRP_summary/SRSF2WTvNBM_alternative_splice_summary.tsv \
  --event_type RI \
  --output_prefix 17_track_visualization/suppa_tracks/RI_colored \
  --psi_column_NBM avg_PSI_NBM \
  --psi_column_mutant avg_PSI_SRSF2WT

# AF events
grep -v "^track" /project/sheynkman/projects/LRP_AML/allAMLvNBM/18_SUPPA/01_splice_events/all.events_AF_strict.gtf > 18_SUPPA/01_splice_events/AF_events.cleaned.gtf
gtfToGenePred 18_SUPPA/01_splice_events/AF_events.cleaned.gtf 17_track_visualization/AF_events.genePred
genePredToBed 17_track_visualization/AF_events.genePred 17_track_visualization/AF_events.bed12
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/AF_events.bed12 \
  --psi_summary 19_LRP_summary/SRSF2WTvNBM_alternative_splice_summary.tsv \
  --event_type AF \
  --output_prefix 17_track_visualization/suppa_tracks/AF_colored \
  --psi_column_NBM avg_PSI_NBM \
  --psi_column_mutant avg_PSI_SRSF2WT

# AL events
grep -v "^track" /project/sheynkman/projects/LRP_AML/allAMLvNBM/18_SUPPA/01_splice_events/all.events_AL_strict.gtf > 18_SUPPA/01_splice_events/AL_events.cleaned.gtf
gtfToGenePred 18_SUPPA/01_splice_events/AL_events.cleaned.gtf 17_track_visualization/AL_events.genePred
genePredToBed 17_track_visualization/AL_events.genePred 17_track_visualization/AL_events.bed12
python 00_scripts/17_color_bed_by_suppa_psi.py \
  --input_bed 17_track_visualization/AL_events.bed12 \
  --psi_summary 19_LRP_summary/SRSF2WTvNBM_alternative_splice_summary.tsv \
  --event_type AL \
  --output_prefix 17_track_visualization/suppa_tracks/AL_colored \
  --psi_column_NBM avg_PSI_NBM \
  --psi_column_mutant avg_PSI_SRSF2WT

#########################################################################
############# rMATS Alternative Splicing Events #########################
#########################################################################
# A3SS events
python 00_scripts/17_rmats_to_long_events.py \
  --input /project/gblab/projects/eAML/scratch/Results/E3999/RNAseq/E3999_SplicingAnalysis/E3999_SplicingAnalysis_KBL/03.splicing/01.rmats_analysis/SFs_WT_vs_Normal/A3SS.MATS.JC.txt \
  --output1 17_track_visualization/rMATS_tracks/A3SS_SFs_WT_rmats.bed12 \
  --output2 17_track_visualization/rMATS_tracks/A3SS_NBM_rmats.bed12 \
  --track_name1 A3SS_SFs_WT_rmats \
  --track_name2 A3SS_NBM_rmats \
  --event_type A3SS

# A5SS events
python 00_scripts/17_rmats_to_long_events.py \
  --input /project/gblab/projects/eAML/scratch/Results/E3999/RNAseq/E3999_SplicingAnalysis/E3999_SplicingAnalysis_KBL/03.splicing/01.rmats_analysis/SFs_WT_vs_Normal/A5SS.MATS.JC.txt \
  --output1 17_track_visualization/rMATS_tracks/A5SS_SFs_WT_rmats.bed12 \
  --output2 17_track_visualization/rMATS_tracks/A5SS_NBM_rmats.bed12 \
  --track_name1 A5SS_SFs_WT_rmats \
  --track_name2 A5SS_NBM_rmats \
  --event_type A5SS

# RI events
python 00_scripts/17_rmats_to_long_events.py \
  --input /project/gblab/projects/eAML/scratch/Results/E3999/RNAseq/E3999_SplicingAnalysis/E3999_SplicingAnalysis_KBL/03.splicing/01.rmats_analysis/SFs_WT_vs_Normal/RI.MATS.JC.txt \
  --output1 17_track_visualization/rMATS_tracks/RI_SFs_WT_rmats.bed12 \
  --output2 17_track_visualization/rMATS_tracks/RI_NBM_rmats.bed12 \
  --track_name1 RI_SFs_WT_rmats \
  --track_name2 RI_NBM_rmats \
  --event_type RI

# MXE events
python 00_scripts/17_rmats_to_long_events.py \
  --input /project/gblab/projects/eAML/scratch/Results/E3999/RNAseq/E3999_SplicingAnalysis/E3999_SplicingAnalysis_KBL/03.splicing/01.rmats_analysis/SFs_WT_vs_Normal/MXE.MATS.JC.txt \
  --output1 17_track_visualization/rMATS_tracks/MXE_SFs_WT_rmats.bed12 \
  --output2 17_track_visualization/rMATS_tracks/MXE_NBM_rmats.bed12 \
  --track_name1 MXE_SFs_WT_rmats \
  --track_name2 MXE_NBM_rmats \
  --event_type MXE

# SE events
python 00_scripts/17_rmats_to_long_events.py \
  --input /project/gblab/projects/eAML/scratch/Results/E3999/RNAseq/E3999_SplicingAnalysis/E3999_SplicingAnalysis_KBL/03.splicing/01.rmats_analysis/SFs_WT_vs_Normal/SE.MATS.JC.txt \
  --output1 17_track_visualization/rMATS_tracks/SE_SFs_WT_rmats.bed12 \
  --output2 17_track_visualization/rMATS_tracks/SE_NBM_rmats.bed12 \
  --track_name1 SE_SFs_WT_rmats \
  --track_name2 SE_NBM_rmats \
  --event_type SE
#  --flank_length 100


#########################################################################
############################ Protein Level ##############################
#########################################################################
# Create files that match the CPM from the edgeR analysis (because CPM is relative to the number of reads in the sample)
# Use filtered protein database - from 13_protein_filter
python 00_scripts/17_filter_DE_proteins.py \
  -i 19_LRP_summary/protein/protein_isoform_DEG_summary_table.tsv \
  --gtf_aml 13_protein_filter/SRSF2_WT_with_cds_filtered.gtf \
  --gtf_nbm 13_protein_filter/NBM_with_cds_filtered.gtf \
  --output_aml 17_track_visualization/SRSF2_WT.edgeR.protein.gtf \
  --output_nbm 17_track_visualization/NBM.edgeR.protein.gtf

## Protein coding gene levels with edgeR CPMs
# Condition 1 - SRSF2_WT
gtfToGenePred 17_track_visualization/SRSF2_WT.edgeR.protein.gtf 17_track_visualization/SRSF2_WT_edgeR_filtered_protein.genePred
genePredToBed 17_track_visualization/SRSF2_WT_edgeR_filtered_protein.genePred 17_track_visualization/SRSF2_WT_edgeR_filtered_protein.bed12
python 00_scripts/17_rgb_by_cpm_to_bed_PB_protein.py --input_bed 17_track_visualization/SRSF2_WT_edgeR_filtered_protein.bed12 --day condition2 --output_file 17_track_visualization/SRSF2_WT_edgeR_filtered_protein.blue.bed12 --sqanti 09_sqanti_protein/SRSF2_WT.sqanti_protein_classification.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/SRSF2_WT_edgeR_filtered_protein.blue.bed12 --output_file 17_track_visualization/SRSF2_WT_edgeR_filtered_protein.cpm.bed12

# Condition 2 - NBM
gtfToGenePred 17_track_visualization/NBM.edgeR.protein.gtf 17_track_visualization/NBM_edgeR_filtered_protein.genePred
genePredToBed 17_track_visualization/NBM_edgeR_filtered_protein.genePred 17_track_visualization/NBM_edgeR_filtered_protein.bed12
python 00_scripts/17_rgb_by_cpm_to_bed_PB_protein.py --input_bed 17_track_visualization/NBM_edgeR_filtered_protein.bed12 --day condition1 --output_file 17_track_visualization/NBM_edgeR_filtered_protein.pink.bed12 --sqanti 09_sqanti_protein/NBM.sqanti_protein_classification.tsv
python 00_scripts/17_cpm_blackred_PB.py --input_bed 17_track_visualization/NBM_edgeR_filtered_protein.pink.bed12 --output_file 17_track_visualization/NBM_edgeR_filtered_protein.cpm.bed12


#########################################################################
########################## Raw Transcripts ##############################
#########################################################################
gtfToGenePred /project/sheynkman/projects/LRP_AML/03_filter_sqanti/AML_corrected.5degfilter.gff 17_track_visualization/AML_raw_transcripts.genePred
genePredToBed 17_track_visualization/AML_raw_transcripts.genePred 17_track_visualization/AML_raw_transcripts.bed12

python 00_scripts/17_unfiltered_transcripts_browser_track.py --input_bed 17_track_visualization/AML_raw_transcripts.bed12 --output_file 17_track_visualization/raw_transcripts/SRSF2_WT_raw_transcripts.bed12 --cpm_file 05_orf_calling/best_ORF_SRSF2WT.tsv
python 00_scripts/17_unfiltered_transcripts_browser_track.py --input_bed 17_track_visualization/AML_raw_transcripts.bed12 --output_file 17_track_visualization/raw_transcripts/NBM_raw_transcripts.bed12 --cpm_file 05_orf_calling/best_ORF_NBM.tsv

#########################################################################
########################## CDS GTF ORFs #################################
#########################################################################
gtfToGenePred 07_make_cds_gtf/SRSF2WT_cds.gtf 17_track_visualization/cds_tracks/SRSF2_WT_cds.genePred
genePredToBed 17_track_visualization/cds_tracks/SRSF2_WT_cds.genePred 17_track_visualization/cds_tracks/SRSF2_WT_cds.bed12
python 00_scripts/17_cds_gtf_blackred.py --input_bed 17_track_visualization/cds_tracks/SRSF2_WT_cds.bed12 --output_file 17_track_visualization/cds_tracks/SRSF2_WT_cds.blackred.bed12 


gtfToGenePred 07_make_cds_gtf/NBM_cds.gtf 17_track_visualization/cds_tracks/NBM_cds.genePred
genePredToBed 17_track_visualization/cds_tracks/NBM_cds.genePred 17_track_visualization/cds_tracks/NBM_cds.bed12
python 00_scripts/17_cds_gtf_blackred.py --input_bed 17_track_visualization/cds_tracks/NBM_cds.bed12 --output_file 17_track_visualization/cds_tracks/NBM_cds.blackred.bed12 


