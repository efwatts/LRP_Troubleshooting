# Long Read Transcriptome Summary <br />
Produces a pacbio accession to gene name reference table. <br />

Here is an AI generated summary of this step: <br />
> The `transcriptome_summary.py` script is designed to generate a summary of the transcriptome data from long-read sequencing. It takes as input various files, including SQANTI classification files, Kallisto TPM files, and gene length statistics. The script processes these inputs to create a comprehensive summary that includes gene-level tables, isoform information, and other relevant metrics. The output files can be used for downstream analysis and visualization of the transcriptome data.
## Input files
- `classification.5degfilter.tsv` - SQANTI3 classification file from [03_filter_sqanti module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti)
- `ensg_gene.tsv` - ENST -> Gene Map file location (from [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))
- `enst_isoname.tsv` - ENST -> Isoname Map file location (from [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))

## Output files
- `pb_gene.tsv` - PacBio accession to gene name reference table
- `sqanti_isoform_info.tsv` - SQANTI isoform information table with gene name

## Required installations
Load modules (if on HPC) and create and activate conda environment. <br />
```
module load gcc/11.4.0
module load miniforge/24.3.0-py3.11
module load openmpi/4.1.4
module load python/3.11.4

conda env create -f ./00_environments/04_transcriptome_sum.yml
conda activate transcriptome_sum
```
## Run Transcriptome Summary from a SLURM script
```
sbatch 00_scripts/04_transcriptome_summary.sh
```
## Or run these commands.
```
python 00_scripts/04_transcriptome_summary_gene_table_only.py \
--sq_out 03_filter_sqanti/sample_collapsed_classification.tsv \
--ensg_to_gene 01_reference_tables/ensg_gene.tsv \
--enst_to_isoname 01_reference_tables/enst_isoname.tsv \
--odir 04_transcriptome_summary/ 

conda deactivate
module purge
```
## Next go to [05_orf-calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling)
### Note: the [04_CPAT module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_CPAT) can be done at this step as well. <br />