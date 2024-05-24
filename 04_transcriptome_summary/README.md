# Long Read Transcriptome Summary - this module can be reduced (see below) <br />
Compares the abundance (CPM) based on long-read sequencing to the abundances (TPM) inferred from short-read sequencing, as computed by Kallisto (analyzed outside of this pipeline). Additionally produces a pacbio-gene reference table. <br />

_Input_
- --sq_out	classification.tsv (from [03_filter_sqanti module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti))
- --tpm	Kallisto TPM file location	(this is a previously obtained input file)
- --ribo	Normalized Kallisto Ribodepletion TPM file location	 (this is a previously obtained input file)
- --ensg_to_gene	ENSG -> Gene Map file location (from [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))
- --enst_to_isoname	ENST -> Isoname Map file location	(from [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))
- --len_stats	Gene Length Statistics table location (from [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))

_Output_
- gene_level_tab.tsv	gene level table	
- sqanti_isoform_info.tsv	sqanti isoform table


## Run Transcriptome Summary
First, build a conda environment and load modules (if using Rivanna or other HPC). <br />
```
module load gcc/11.4.0
module load mamba/22.11.1-4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11
module load openmpi/4.1.4
module load python/3.11.4

conda env create -f ./00_environments/04_transcriptome_sum.yml
conda activate transcriptome_sum
```
Then call the python script either using `04_transcriptome_summary.sh` or the following command: <br />
```
python ./00_scripts/04_transcriptome_summary.py \
--sq_out ./03_filter_sqanti/jurkat_classification.tsv \
--tpm ./00_input_data/jurkat_gene_kallisto.tsv \
--ribo ./00_input_data/kallist_table_rdeplete_jurkat.tsv \
--ensg_to_gene ./01_reference_tables/ensg_gene.tsv \
--enst_to_isoname ./01_reference_tables/enst_isoname.tsv \
--len_stats ./01_reference_tables/gene_lens.tsv \
--odir ./04_transcriptome_summary/

conda deactivate
```
## Next go to [05_orf-alling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling)
### Note: the [04_CPAT module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_CPAT) or [04_six_frame_translation module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_six_frame_translation) can be done at this stage as well. 

# If you only need the table 'pb_gene.tsv' (this name will likely change in the future), run the module this way
Compile data for downstream analyses. <br />
_Input_
- --sq_out	classification.txt file (from [02_SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_SQANTI))
- --ensg_to_gene	ENSG -> Gene Map file location (from [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))
- --enst_to_isoname	ENST -> Isoname Map file location	(from [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))

_Output_
- gene_level_tab.tsv	gene level table	
- sqanti_isoform_info.tsv	sqanti isoform table

- ## Run Transcriptome Summary

First, build a conda environment and load modules (if using Rivanna or other HPC). <br />
```
module load gcc/11.4.0
module load mamba/22.11.1-4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11
module load openmpi/4.1.4
module load python/3.11.4

conda env create -f ./00_environments/04_transcriptome_sum.yml
conda activate transcriptome_sum
```
Then call the python script either using the following command: <br />
```
python ./00_scripts/04_transcriptome_summary_gene_table_only.py \
--sq_out ./03_filter_sqanti/jurkat_classification.txt \
--ensg_to_gene ./01_reference_tables/ensg_gene.tsv \
--enst_to_isoname ./01_reference_tables/enst_isoname.tsv \
--odir ./03_transcriptome_summary/

conda deactivate
```
