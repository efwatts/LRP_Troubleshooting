# Reference Tables
This step can be done at the beginning of the pipeline to generate reference tables to be used as input at other stages. <br />
Here is an AI generated summary of this step: <br />
> The `prepare_reference_tables.py` script is designed to generate reference tables from Gencode GTF and transcript FASTA files. It processes the GTF file to extract gene and transcript information, including gene IDs, transcript IDs, and their corresponding protein sequences. The script also calculates the lengths of transcripts and genes, creating several output tables that can be used for downstream analysis in RNA-seq studies. The generated tables include mappings between gene IDs and transcript IDs, as well as length statistics for transcripts and genes.
> The script takes as input a GTF file and a transcript FASTA file, and produces several output files, including:
> - `ensg_gene.tsv`: Mapping of Ensembl gene IDs to gene names.
> - `enst_isoname.tsv`: Mapping of Ensembl transcript IDs to isonames.
> - `gene_ensp.tsv`: Mapping of gene names to Ensembl protein IDs.
> - `gene_isoname.tsv`: Mapping of gene names to isonames.
> - `isoname_lens.tsv`: Length statistics for isonames.
> - `gen_lens.tsv`: Length statistics for genes.
> - `protein_coding_genes.txt`: List of protein-coding genes.

## Input files <br />
You will need the following input files:_ <br />
- [Gencode](https://www.gencodegenes.org/) GTF file _--gtf_
- [Gencode](https://www.gencodegenes.org/) transcripts fasta file _--fa_

## Required installations: <br />
Load modules (if on HPC) and create and activate conda environment. <br />
```
module load isoseqenv/py3.7
module load apptainer/1.3.4
module load gcc/11.4.0
module load bedops/2.4.41
module load nseg/1.0.0
module load openmpi/4.1.4
module load python/3.11.4 
module load miniforge/24.3.0-py3.11

conda env create -f 00_environments/reference_tables.yml
conda activate reference_tab
```
Load Docker (here using Apptainer). <br />
```
apptainer pull docker://gsheynkmanlab/generate-reference-tables:latest
```
## Run reference tables from a SLURM script <br />
```
sbatch 00_scripts/01_reference_tables.sh
```
## Or run these commands. <br />
Note, this is where the docker image lives on the Sheynkman lab server. If you are using a different server, you will need to change the path to the docker image. <br />
```
apptainer exec /project/sheynkman/dockers/LRP/generate-reference-tables_latest.sif /bin/bash -c "\
    python 00_scripts/01_prepare_reference_tables.py \
        --gtf /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
        --fa /project/sheynkman/external_data/GENCODE_v47/gencode.v47.pc_transcripts.fa \
        --ensg_gene 01_reference_tables/ensg_gene.tsv \
        --enst_isoname 01_reference_tables/enst_isoname.tsv \
        --gene_ensp 01_reference_tables/gene_ensp.tsv \
        --gene_isoname 01_reference_tables/gene_isoname.tsv \
        --isoname_lens 01_reference_tables/isoname_lens.tsv \
        --gene_lens 01_reference_tables/gene_lens.tsv \
        --protein_coding_genes 01_reference_tables/protein_coding_genes.txt
"
exit
conda deactivate
```

## Next go to [SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_sqanti) or [Make Gencode Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_make_gencode_database)
### Note: the [Iso-Seq module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_isoseq) can be done at this stage as well. 
