# Aggregated 6-frame translation <br />
Generates a fasta file of all possible protein sequences derivable from each PacBio transcript, by translating the fasta file in all six frames (3+, 3-). This is used to examine what peptides could theoretically match the peptides found via a mass spectrometry search against GENCODE. <br />

_Input_
- Isoform classification table, classification.tsvv (from [03_filter_sqanti module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti))
- corrected.fasta (from [03_filter_sqanti module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti))
- ensg to gene table (from [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))

_Output_
- FASTA of the "protein space" for each gene (pacbio_6frm_database_gene_grouped.fasta)

## Run 6-frame translation
First, build a conda environment and load modules (if using Rivanna or other HPC). <br />
```
module load gcc/11.4.0
module load mamba/22.11.1-4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11
module load openmpi/4.1.4
module load python/3.11.4

conda env create -f ./00_environments/04_6frame.yml
conda activate 6frame
```
Then call the python script either using `04_six_frame_translation.sh` or the following command: <br />
```
python ./00_scripts/04_six_frame_translation.py \
--iso_annot ./03_filter_sqanti/jurkat_classification.tsv \
--ensg_gene ./01_reference_tables/ensg_gene.tsv \
--sample_fasta ./03_filter_sqanti/jurkat_corrected.fasta \
--output_fasta ./04_six_frame_translation/pacbio_6frm_database_gene_grouped.fasta

conda deactivate
```
## Next go to [05_orf-calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling)
### Note: the [04_CPAT module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_CPAT) or [04_transcriptome_summary module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_transcriptome_summary) can be done at this stage as well. 
