# LRP Visualization of Differential Gene Expression (DGE), Differential Transcript Expression (DTE), and Differential Transcript Usage (DTU)
This module is desigened to look at DGE, DTE, and DTU from the results of the LRP pipeline. This is the newest module in the pipeline and is still being developed and automated. Any feedback is welcome! This module is run using R Markdown. <br />
Here is an AI generated summary of this step: <br />
> The `19_LRP_summary` module is designed to analyze and summarize differential expression and splicing events in RNA-Seq data. It includes scripts for differential transcript expression (DTE), differential gene expression (DGE), isoform fraction calculation, and dropout summarization. The module generates summary tables that integrate results from various analyses, providing insights into gene and transcript-level expression changes across different conditions. The output files include DTE and DGE results, isoform fractions, dropout summaries, and a comprehensive summary table for downstream analysis.
## Input files
- `merged.collapsed.flnc_count.txt` - collapsed Iso-Seq file from the [01 Iso-Seq module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_isoseq)
- `sample_classification.5degfilter.tsv` - classification file from the [03 Filter SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti)
- `ensg_gene.tsv` - GENCODE gene information file from the [01 Make Reference Tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables)

## Required installations
Load modules (if on HPC) and create and activate conda environment. <br />
```
module load gcc/11.4.0 openmpi/4.1.4 python/3.11.4 miniforge/24.3.0-py3.11 samtools/1.17 R/4.5.0
```
## Run from command line or run locally via RStudio
```
Rscript 00_scripts/20_DTE_DGE.R
```