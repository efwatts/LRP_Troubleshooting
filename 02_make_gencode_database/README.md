# Make Gencode Database
This module creases a database of proteins clustered by gene from the Gencode translations file and the list protein coding genes from the [Reference Tables](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables) 
module. This database will be used in downstream modules. <br />

Here is an AI generated summary of this step: <br />
> The `make_gencode_database.py` script is designed to create a clustered protein database from Gencode translation sequences. It takes as input a FASTA file containing protein sequences and a list of protein-coding genes, and generates a clustered FASTA file and a table of clustered isonames. The script uses the `cd-hit` tool to cluster the sequences based on their similarity, allowing for the identification of redundant or similar sequences. The output files can be used for downstream analysis in proteomics and transcriptomics studies.
## Input files
- `gencode.v46.pc_translations.fa` - Gencode translations fasta file (from [Gencode](https://www.gencodegenes.org/))
- `protein_coding_genes.txt` - List of protein coding genes (from [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))

## Required installations 
Load modules (if on HPC) and create and activate conda environment. <br />
```
module load gcc/11.4.0
module load openmpi/4.1.4
module load python/3.11.4 
module load miniforge/24.3.0-py3.11
module load perl/5.36.0 
module load star/2.7.9a 
module load kallisto/0.48.0

conda env create -f 00_environments/make_gencode_database.yml
conda activate make_database
```
## Create gencode database from a SLURM script <br />
```
sbatch 00_scripts/02_make_gencode_database.sh
```
## Or run these commands. <br />
```
python 00_scripts/02_make_gencode_database.py \
--gencode_fasta /project/sheynkman/external_data/GENCODE_v47/gencode.v47.pc_transcripts.fa \
--protein_coding_genes 01_reference_tables/protein_coding_genes.txt \
--output_fasta 02_make_gencode_database/gencode_clusters.fasta \
--output_cluster 02_make_gencode_database/gencode_isoname_clusters.tsv

conda deactivate
```

## Next go to [Filter SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti)
### Note: the [SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_sqanti) can be done at this stage as well. 
