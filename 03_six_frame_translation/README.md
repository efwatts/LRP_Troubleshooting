# Aggregated 6-frame translation <br />
Derives the "protein space" from pacbio data. <br />
_Input_
- Isoform classification table, classification.txt (from [02_SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_SQANTI))
- corrected.fasta (from [02_SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_SQANTI))
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

conda env create -f ./00_environments/6frame.yml
conda activate 6frame
```
Then call the python script either using `03_six_frame_translation.sh` or the following command: <br />
```
python ./00_scripts/six_frame_translation.py \
--iso_annot ./02_sqanti/output/jurkat_classification.txt \
--ensg_gene ./01_reference_tables/ensg_gene.tsv \
--sample_fasta ./02_sqanti/output/jurkat_corrected.fasta \
--output_fasta ./03_six_frame_translation/pacbio_6frm_database_gene_grouped.fasta

conda deactivate
```
## Next go to [ORF-Calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_orf-calling)
### Note: the [CPAT module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_CPAT) or [Transcriptome Summary module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_transcriptome_summary) can be done at this stage as well. 
