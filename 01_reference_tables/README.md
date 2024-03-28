# Reference Tables
This step can be done at the beginning of the pipeline to generate reference tables to be used as input at other stages. <br />
_Input:_ <br />
- [Gencode](https://www.gencodegenes.org/) GTF file _--gtf_
- [Gencode](https://www.gencodegenes.org/) transcripts fasta file _--fa_

_Output:_ <br />
- Series of gene tables
  --ensg_gene	ensg to gene 
  --enst_isoname	enst to isoname 
  --gene_ensp	Gene to ensp 
  --gene_isoname	Gene to isoname 
  --isoname_lens	Isoname length table 
  --gen_lens	Gene Length statistics 

## Create reference tables
Step 1: Create and activate conda environment. I am also setting my working directory here, because you can never be too careful with that! <br />
```
cd /project/sheynkman/users/emily/LRP_test/jurkat
conda env create -f ./00_environments/reference_tables.yml
conda activate reference_tab
```
Step 2: Call `prepare_reference_tables.py` with `01_reference_tables.sh` if using Rivanna or other HPC or run this command, changing file locations appropriately. <br />
```
python ./00_scripts/prepare_reference_tables.py \
--gtf ./00_input_data/gencode.v35.annotation.canonical.gtf \
--fa ./00_input_data/gencode.v35.pc_transcripts.fa \
--ensg_gene ./01_reference_tables/ensg_gene.tsv \
--enst_isoname ./01_reference_tables/enst_isoname.tsv \
--gene_ensp ./01_reference_tables/gene_ensp.tsv \
--gene_isoname ./01_reference_tables/gene_isoname.tsv \
--isoname_lens ./01_reference_tables/isoname_lens.tsv \
--gene_lens ./01_reference_tables/gene_lens.tsv \
--protein_coding_genes ./01_reference_tables/protein_coding_genes.txt

conda deactivate
```
