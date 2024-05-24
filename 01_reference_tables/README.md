# Reference Tables
This step can be done at the beginning of the pipeline to generate reference tables to be used as input at other stages. <br />

_Input:_ <br />
- [Gencode](https://www.gencodegenes.org/) GTF file _--gtf_
- [Gencode](https://www.gencodegenes.org/) transcripts fasta file _--fa_

_Output:_ <br />
Series of gene tables
  - --ensg_gene	ensg to gene 
  - --enst_isoname	enst to isoname 
  - --gene_ensp	Gene to ensp 
  - --gene_isoname	Gene to isoname 
  - --isoname_lens	Isoname length table 
  - --gen_lens	Gene Length statistics 

## Create reference tables
Step 1: Load modules (if on HPC) and create and activate conda environment. <br />
```
cd /project/sheynkman/users/emily/LRP_test/jurkat

module load isoseqenv/py3.7
module load apptainer/1.2.2
module load gcc/11.4.0
module load bedops/2.4.41
module load mamba/22.11.1-4
module load nseg/1.0.0
module load bioconda/py3.10
module load anaconda/2023.07-py3.11
module load openmpi/4.1.4
module load python/3.11.4

conda env create -f ./00_environments/reference_tables.yml
conda activate reference_tab
```
Step 2: Load Docker (here using Apptainer). <br />
```
apptainer pull docker://gsheynkmanlab/generate-reference-tables:latest
```
Step 3: Enter the Docker and call `prepare_reference_tables.py` with `01_reference_tables.sh` if using Rivanna or other HPC or run this command, changing file locations appropriately. <br />
```
apptainer exec generate-reference-tables_latest.sif /bin/bash -c "\
    python ./00_scripts/01_prepare_reference_tables.py \
        --gtf ./00_input_data/gencode.v46.annotation.gtf \
        --fa ./00_input_data/gencode.v46.pc_transcripts.fa \
        --ensg_gene ./01_reference_tables/ensg_gene.tsv \
        --enst_isoname ./01_reference_tables/enst_isoname.tsv \
        --gene_ensp ./01_reference_tables/gene_ensp.tsv \
        --gene_isoname ./01_reference_tables/gene_isoname.tsv \
        --isoname_lens ./01_reference_tables/isoname_lens.tsv \
        --gene_lens ./01_reference_tables/gene_lens.tsv \
        --protein_coding_genes ./01_reference_tables/protein_coding_genes.txt
"
exit
conda deactivate
```

## Next go to [SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_SQANTI) or [Make Gencode Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_make_gencode_database)
### Note: the [Iso-Seq module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_Iso-Seq) can be done at this stage as well. 
