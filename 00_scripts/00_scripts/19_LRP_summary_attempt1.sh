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
module load gcc/11.4.0
module load bedops/2.4.41
module load nseg/1.0.0
module load openmpi/4.1.4
module load python/3.11.4 
module load miniforge/24.3.0-py3.11
module load R/4.4.1

conda activate reference_tab

# First, do protein isoform levels
# Step 1 - align CDS_GTF file with SQANTI classification output (need CPM for each biological sample, and need each biological sample to be renamed as X504_Q157R, A258_Q157R, A309_Q157R, V335_WT, V334_WT, and A310_WT) and gene name and transcript from sqanti_isoform_info.tsv
python 00_scripts/19_summary_table.py -s 03_filter_sqanti/MDS_classification.5degfilter.tsv -w 07_make_cds_gtf/Q157R_cds.gtf -m 07_make_cds_gtf/WT_cds.gtf -i 04_transcriptome_summary/sqanti_isoform_info.tsv -o 19_LRP_summary/protein_isoform_summary.tsv

# Step 2 - gene counts table with gene name and CPM for each biological sample
python 00_scripts/19_sum_gene_cpm.py -i 19_LRP_summary/protein_isoform_summary.tsv -o 19_LRP_summary/protein_gene_cpm_summary.tsv -s X504_Q157R,A258_Q157R,A309_Q157R,V335_WT,V334_WT,A310_WT

# Step 3 - isoform fractional abundance table with transcript name and CPM for each biological sample
python /project/sheynkman/projects/LRP_Mohi_project/00_scripts/19_calculate_isoform_fractions.py -i /project/sheynkman/projects/LRP_Mohi_project/19_LRP_summary/protein_isoform_summary.tsv -o 19_LRP_summary/protein_isoform_fractions.tsv

# Step 4 - differential expression 
    # bring transcript counts table to edgeR and generate differential gene expression with average WT and mutant samples with p-values
    # First run edgeR script - if you run it this way, you need to edit it manually first
Rscript 19_LRP_summary/edgeR/edgeR.R 

python 00_scripts/19_diff_transcript_expression.py \
    -s 19_LRP_summary/protein_isoform_summary.tsv \
    -e 19_LRP_summary/edgeR/transcript_DEG_results.txt \
    -o 19_LRP_summary/protein_diff_isoform_expression.tsv

python 00_scripts/19_diff_gene_expression.py \
    -s 19_LRP_summary/protein_isoform_summary.tsv \
    -e 19_LRP_summary/edgeR/gene_DEG_results.txt \
    -o 19_LRP_summary/protein_diff_gene_expression.tsv


# Now, do transcript isoform levels
# Step 1 - format filter SQANTI output (need CPM for each biological sample, and need each biological sample to be renamed as X504_Q157R, A258_Q157R, A309_Q157R, V335_WT, V334_WT, and A310_WT) and gene name and transcript from sqanti_isoform_info.tsv
python 00_scripts/19_summary_table.py -s 03_filter_sqanti/MDS_classification.5degfilter.tsv -w 17_track_visualization/WT.filter_sqanti.gtf -m 17_track_visualization/Q157R.filter_sqanti.gtf -i 04_transcriptome_summary/sqanti_isoform_info.tsv -o 19_LRP_summary/transcript_isoform_summary.tsv

# Step 2 - gene counts table with gene name and CPM for each biological sample
python 00_scripts/19_sum_gene_cpm.py -i 19_LRP_summary/transcript_isoform_summary.tsv -o 19_LRP_summary/transcript_gene_cpm_summary.tsv -s X504_Q157R,A258_Q157R,A309_Q157R,V335_WT,V334_WT,A310_WT

# Step 3 - isoform fractional abundance table with transcript name and CPM for each biological sample
python /project/sheynkman/projects/LRP_Mohi_project/00_scripts/19_calculate_isoform_fractions.py -i /project/sheynkman/projects/LRP_Mohi_project/19_LRP_summary/transcript_isoform_summary.tsv -o 19_LRP_summary/transcript_isoform_fractions.tsv

# Step 4 - differential expression 
    # Use the same edgeR output from above (this info is unchanged)

python 00_scripts/19_diff_transcript_expression.py \
    -s 19_LRP_summary/transcript_isoform_summary.tsv \
    -e 19_LRP_summary/edgeR/transcript_DEG_results.txt \
    -o 19_LRP_summary/transcript_diff_isoform_expression.tsv

python 00_scripts/19_diff_gene_expression.py \
    -s 19_LRP_summary/transcript_isoform_summary.tsv \
    -e 19_LRP_summary/edgeR/gene_DEG_results.txt \
    -o 19_LRP_summary/transcript_diff_gene_expression.tsv

conda deactivate
module purge