#!/bin/bash

#SBATCH --job-name=19_LRP_summary
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

# Load necessary modules (if needed)
module purge
module load gcc
module load bedops
module load nseg
module load openmpi
module load python
module load miniforge
module load R

conda activate reference_tab

######################################################
###############Transcript Level Analysis##############
######################################################
# Create raw gene counts matrix
python 00_scripts/19_raw_gene_counts.py \
    03_filter_sqanti/MDS_filtered_raw_counts.tsv \
    19_LRP_summary/edgeR/raw_gene_counts_matrix.txt 

# Run edgeR for transcript level analysis
# Note: this script is required to be run inside of R at this time. I need to convert the Rmd file to a script and rearrange inputs.
Rscript 19_LRP_summary/edgeR/19_edgeR_summary.Rmd

# Create transcript isoform level DEG summary
python 00_scripts/19_transcript_DEG_summary.py \
  --cpm 19_LRP_summary/edgeR/edgeR_transcript/normalized_CPM_matrix.txt \
  --deg 19_LRP_summary/edgeR/edgeR_transcript/transcript_DEG_results.txt \
  --class 03_filter_sqanti/MDS_classification.5degfilter.tsv \
  --gene_map 01_reference_tables/ensg_gene.tsv \
  --output 19_LRP_summary/transcript_DEG_summary_table.tsv \
  --wt_samples V335_WT V334_WT A310_WT \
  --q157r_samples X504_Q157R A258_Q157R A309_Q157R \
  --rename_samples \
    BioSample_1=V334_WT \
    BioSample_2=A258_Q157R \
    BioSample_3=A310_WT \
    BioSample_4=V335_WT \
    BioSample_5=X504_Q157R \
    BioSample_6=A309_Q157R

# Create gene level DEG summary
python 00_scripts/19_gene_DEG_summary.py \
  --cpm 19_LRP_summary/edgeR/edgeR_gene/normalized_CPM_matrix_gene.txt \
  --deg 19_LRP_summary/edgeR/edgeR_gene/gene_DEG_results.txt \
  --class 03_filter_sqanti/MDS_classification.5degfilter.tsv \
  --gene_map 01_reference_tables/ensg_gene.tsv \
  --output 19_LRP_summary/gene_DEG_summary_table.tsv \
  --wt_samples V335_WT V334_WT A310_WT \
  --q157r_samples X504_Q157R A258_Q157R A309_Q157R \
  --rename_samples \
    BioSample_1=V334_WT \
    BioSample_2=A258_Q157R \
    BioSample_3=A310_WT \
    BioSample_4=V335_WT \
    BioSample_5=X504_Q157R \
    BioSample_6=A309_Q157R

# Run DRIMSeq for DTU analysis
# Note: this script is required to be run inside of R at this time. I need to convert the Rmd file to a script and rearrange inputs.
Rscript 19_LRP_summary/DRIMSeq/19_DRIMSeq.Rmd

# Create transcript isoform level DTU summary
python 00_scripts/19_transcript_DTU_summary.py \
  --deg_summary 19_LRP_summary/transcript_DEG_summary_table.tsv \
  --dtu 19_LRP_summary/DRIMSeq/drimseq_transcript_results.tsv \
  --output 19_LRP_summary/transcript_DTU_summary.tsv

# Create alternative splicing summary
python 00_scripts/19_SUPPA_summary.py \
  --psivec 18_SUPPA/MDS_diffsplice.psivec \
  --dpsi 18_SUPPA/MDS_diffsplice.dpsi \
  --sqanti 03_filter_sqanti/MDS_classification.5degfilter.tsv \
  --gene_map 01_reference_tables/ensg_gene.tsv \
  --output 19_LRP_summary/alternative_splice_summary.tsv \
  --cond1_name Q157R \
  --cond2_name WT

# Now, create summary figures using the results from the above analyses
# Note: these scripts are required to be run inside of R at this time. I need to convert the Rmd filse to scripts and rearrange inputs.
Rscript 19_LRP_summary/19_heatmaps.Rmd
Rscript 19_LRP_summary/correlation_matrices.Rmd
Rscript 19_LRP_summary/19_barplots.Rmd

# Can also generate summary figures for significant alternative splicing events
python /project/sheynkman/programs/SUPPA-2.4/scripts/generate_boxplot_event.py -i 18_SUPPA/combined_local.psi -e "PB.10012;SE:chr6:134992903-134993545:134993616-134994084:+" -g 1-3,4-6 -c condition1,condition2 -o 18_SUPPA/


######################################################
###############Protein Level Analysis##############
######################################################
# Create raw protein counts matrix
python 00_scripts/19_raw_gene_counts.py \
    06_refine_orf_database/protein_counts_matrix.csv \
    19_LRP_summary/protein/raw_protein_gene_counts_matrix.txt 

# Create filtered protein counts matrix
# isoform
python 00_scripts/19_filter_protein_isoform_counts.py \
    --counts 06_refine_orf_database/protein_counts_matrix.csv \
    --metadata 13_protein_filter/Q157R.classification_filtered.tsv \
    --output 19_LRP_summary/protein/filtered_protein_isoform_counts_matrix.txt

# gene
python 00_scripts/19_filter_protein_counts.py \
    --counts 19_LRP_summary/protein/raw_protein_gene_counts_matrix.txt \
    --metadata 13_protein_filter/Q157R.classification_filtered.tsv \
    --output 19_LRP_summary/protein/filtered_protein_gene_counts_matrix.txt

# Run edgeR for transcript level analysis
# Note: this script is required to be run inside of R at this time. I need to convert the Rmd file to a script and rearrange inputs.
Rscript 19_LRP_summary/protein/edgeR/19_edgeR_summary.Rmd

# Create isoform level DEG summary for protein
python 00_scripts/19_protein_isoform_DEG_summary.py \
  --cpm 19_LRP_summary/protein/edgeR/protein_isoform_dpe_results/normalized_CPM_matrix.tsv \
  --deg 19_LRP_summary/protein/edgeR/protein_isoform_dpe_results/protein_isoform_DPE_results.tsv \
  --class 09_sqanti_protein/WT.sqanti_protein_classification.tsv \
  --gene_map 01_reference_tables/ensg_gene.tsv \
  --output 19_LRP_summary/protein/protein_isoform_DEG_summary_table.tsv \
  --wt_samples V335_WT V334_WT A310_WT \
  --q157r_samples X504_Q157R A258_Q157R A309_Q157R \
  --rename_samples \
    BioSample_1=V334_WT \
    BioSample_2=A258_Q157R \
    BioSample_3=A310_WT \
    BioSample_4=V335_WT \
    BioSample_5=X504_Q157R \
    BioSample_6=A309_Q157R

# Create gene level DEG summary for protein
python 00_scripts/19_gene_protein_DEG_summary.py \
  --cpm 19_LRP_summary/protein/edgeR/protein_gene_dpe_results/normalized_CPM_matrix.tsv \
  --deg 19_LRP_summary/protein/edgeR/protein_gene_dpe_results/protein_gene_DPE_results.tsv \
  --class 09_sqanti_protein/WT.sqanti_protein_classification.tsv \
  --gene_map 01_reference_tables/ensg_gene.tsv \
  --output 19_LRP_summary/protein/protein_gene_DEG_summary_table.tsv \
  --wt_samples V335_WT V334_WT A310_WT \
  --q157r_samples X504_Q157R A258_Q157R A309_Q157R \
  --rename_samples \
    BioSample_1=V334_WT \
    BioSample_2=A258_Q157R \
    BioSample_3=A310_WT \
    BioSample_4=V335_WT \
    BioSample_5=X504_Q157R \
    BioSample_6=A309_Q157R

# Run DRIMSeq for DTU analysis
# Note: this script is required to be run inside of R at this time. I need to convert the Rmd file to a script and rearrange inputs.
Rscript 19_LRP_summary/protein/DRIMSeq/19_DRIMSeq.Rmd

# Create isoform level DTU summary for protein
python 00_scripts/19_transcript_DTU_summary.py \
  --deg_summary 19_LRP_summary/protein/protein_isoform_DEG_summary_table.tsv \
  --dtu 19_LRP_summary/protein/DRIMSeq/drimseq_protein_tx_results.tsv \
  --output 19_LRP_summary/protein/protein_isoform_DTU_summary.tsv

# Now, create summary figures using the results from the above analyses
# Note: these scripts are required to be run inside of R at this time. I need to convert the Rmd filse to scripts and rearrange inputs.
Rscript 19_LRP_summary/protein/19_heatmaps.Rmd
Rscript 19_LRP_summary/protein/correlation_matrices.Rmd
Rscript 19_LRP_summary/protein/19_barplots.Rmd

conda deactivate
module purge

