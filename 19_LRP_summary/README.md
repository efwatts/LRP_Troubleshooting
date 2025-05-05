# LRP Summary
This module summarizes the results of the LRP pipeline. It includes a summary of the number of genes and transcripts detected, as well as the number of differentially expressed genes and transcripts. The module also includes a summary of the number of splicing events detected by SUPPA. <br />
This also includes a script to count the genes from Iso-Seq for gene-level summaries. This is currently a manual step, but I plan to automate this in the future. <br />
Here is an AI generated summary of this step: <br />
### Detailed Script Summaries
#### 19_diff_transcript_expression.py
- **Purpose**: Performs differential transcript expression (DTE) analysis.
- **Key Steps**:
  1. Reads transcript-level expression data (e.g., CPM or TPM).
  2. Applies statistical tests to identify transcripts with significant expression changes between conditions.
  3. Outputs a table of differentially expressed transcripts with associated statistics (e.g., log fold change, p-value, adjusted p-value).
- **Inputs**: Transcript expression matrix, condition metadata.
- **Outputs**: DTE results table.

#### 19_diff_gene_expression.py
- **Purpose**: Performs differential gene expression (DGE) analysis.
- **Key Steps**:
  1. Aggregates transcript-level expression data to the gene level.
  2. Applies statistical tests to identify genes with significant expression changes between conditions.
  3. Outputs a table of differentially expressed genes with associated statistics.
- **Inputs**: Gene expression matrix, condition metadata.
- **Outputs**: DGE results table.

#### 19_calculate_isoform_fractions.py
- **Purpose**: Calculates isoform fractions for each gene.
- **Key Steps**:
  1. Computes the proportion of each isoform's expression relative to the total expression of its parent gene.
  2. Outputs a table with isoform fractions for each condition.
- **Inputs**: Transcript expression matrix, gene-to-isoform mapping.
- **Outputs**: Isoform fraction table.

#### 19_sum_gene_cpm.py
- **Purpose**: Sums transcript-level CPM values to calculate gene-level CPM.
- **Key Steps**:
  1. Aggregates CPM values for all isoforms of a gene.
  2. Outputs a table with gene-level CPM values for each condition.
- **Inputs**: Transcript-level CPM matrix, gene-to-isoform mapping.
- **Outputs**: Gene-level CPM table.

#### 19_summarize_dropouts.py
- **Purpose**: Summarizes dropout events (genes or transcripts with zero expression in certain conditions).
- **Key Steps**:
  1. Identifies genes or transcripts with zero expression in one or more conditions.
  2. Outputs a summary table with dropout statistics.
- **Inputs**: Expression matrix (transcript or gene level).
- **Outputs**: Dropout summary table.

#### 19_summary_table.py
- **Purpose**: Integrates results from multiple analyses into a comprehensive summary table.
- **Key Steps**:
  1. Combines DTE, DGE, isoform fractions, and dropout summaries.
  2. Generates a final table summarizing key metrics for each gene and transcript.
- **Inputs**: Outputs from the above scripts (DTE, DGE, isoform fractions, CPM, dropouts).
- **Outputs**: Final summary table for downstream analysis.

## Input files
- `sample_classification.5degfilter.tsv` - classification file from the [03 Filter SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti)
- `sqanti_isoform_info.tsv` - isoform information file from the [04 Transcriptome Summary module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_transcriptome_summary)
- `condition1_cds.gtf` - GTF file with CDS annotations for each sample. This file is generated from the [07 Make CDS GTF module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_make_cds_gtf)
- `condition2_cds.gtf` - GTF file with CDS annotations for each sample. This file is generated from the [07 Make CDS GTF module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_make_cds_gtf)

## Required installations
Load modules (if on HPC) and activate conda environment. <br />
```
module load gcc/11.4.0
module load bedops/2.4.41
module load nseg/1.0.0
module load openmpi/4.1.4
module load python/3.11.4 
module load miniforge/24.3.0-py3.11
module load R/4.4.1

conda activate reference_tab
```
## Run LRP Summary from a SLURM script
Be sure to edit the `00_scripts/19_LRP_summary.sh` script to include the correct paths for your input files and edit R script first. <br />
```
sbatch 00_scripts/19_LRP_summary.sh
```
## Or run these commands.
Note: I sometimes have trouble running R scripts from the HPC, because of package installations, so I often run the R scripts locally. <br />
```
# Step 0 - make gene counts from isoseq
python sum_gene_cpm.py \
  -i input_cpm.tsv \
  -o output_gene_cpm.tsv \
  -s sample1_name,sample2_name,sample3_name,sample4_name,sample5_name,sample6_name \

# Step 1 - align CDS_GTF file with SQANTI classification output (need CPM for each biological sample, and need each biological sample to be renamed as X504_Q157R, A258_Q157R, A309_Q157R, V335_WT, V334_WT, and A310_WT) and gene name and transcript from sqanti_isoform_info.tsv
python 00_scripts/19_summary_table.py -s 03_filter_sqanti/sample_classification.5degfilter.tsv -w 07_make_cds_gtf/condition1_cds.gtf -m 07_make_cds_gtf/condition2_cds.gtf -i 04_transcriptome_summary/sqanti_isoform_info.tsv -o 19_LRP_summary/full_summary.tsv

# Step 2 - gene counts table with gene name and CPM for each biological sample
python 00_scripts/19_sum_gene_cpm.py -i 19_LRP_summary/full_summary.tsv -o 19_LRP_summary/gene_cpm_summary.tsv

# Step 3 - isoform fractional abundance table with transcript name and CPM for each biological sample
python 00_scripts/19_calculate_isoform_fractions.py -i 19_LRP_summary/full_summary.tsv -o 19_LRP_summary/isoform_fractions.tsv

# Step 4 - differential expression 
    # bring transcript counts table to edgeR and generate differential gene expression with average WT and mutant samples with p-values
    # First run edgeR script - if you run it this way, you need to edit it manually first
Rscript 19_LRP_summary/edgeR/edgeR_script.R 

python 00_scripts/19_diff_transcript_expression.py \
    -s 19_LRP_summary/full_summary.tsv \
    -e 19_LRP_summary/edgeR/edgeR_transcript_results.csv \
    -o 19_LRP_summary/diff_transcript_expression.tsv

python 00_scripts/19_diff_gene_expression.py \
    -s 19_LRP_summary/full_summary.tsv \
    -e 19_LRP_summary/edgeR/gene_DEG_results.txt \
    -o 19_LRP_summary/diff_gene_expression.tsv

conda deactivate
module purge
```
Proceed to [20 Visualization](https://github.com/efwatts/LRP_Troubleshooting/tree/main/20_visualization)