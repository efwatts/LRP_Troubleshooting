# Make Gencode Database
This module creases a database of proteins clustered by gene from the Gencode translations file and the list protein coding genes from the [Reference Tables](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables) 
module. This database will be used in downstream modules. <br />
_Input:_ 
- Gencode translations fasta (from Gencode)
- List of protein coding genes (from Reference Tables module)
_Output:_
- Clustered fasta file (gencode_clusters.fasta)
- Table of clustered isonames (gencode_isoname_clusters.tsv)

## Create gencode database
Step 1: Create and activate conda environmnet.
```
cd /project/sheynkman/users/emily/LRP_test/jurkat

conda env create -f ./00_environments/make_gencode_database.yml
conda activate make_database
```
Step 2: Run `02_make_gencode_database.sh` to call `make_gencode_database.py` if using Rivanna or other HPC or run this command:
```
python ./00_scripts/make_gencode_database.py \
--gencode_fasta ./00_input_data/gencode.v37.pc_translations.fa \
--protein_coding_genes ./01_reference_tables/protein_coding_genes.txt \
--output_fasta ./02_make_gencode_database/gencode_clusters.fasta \
--output_cluster ./02_make_gencode_database/gencode_isoname_clusters.tsv
```
