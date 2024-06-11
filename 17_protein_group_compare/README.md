# Protein Group Comparison 
Determine the relationship between protein groups identified in Metamorpheus using GENCODE, UniProt, and/or PacBio databases

_Input:_ <br />
- AllQuantifiedProteinGroups.Gencode.tsv (from [16 MetaMorpheus module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/16_MetaMorpheus))
- AllQuantifiedProteinGroups.sample.tsv (refined, hybrid, and/or filtered) (from [16 MetaMorpheus module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/16_MetaMorpheus))
- accession_map_gencode_uniprot_pacbio.tsv (from [15 Accession Mapping module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/15_accession_mapping))
  
_Output:_
- comparison.xlsx (one for each comparison)

## Run script
If running on Rivanna or other HPC, load required modules. Make a conda environment.
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11

conda create -n group_comp python pandas openpyxl
conda activate group_comp
pip install xlsxwriter
```
Run the script. I am doing 3 examples here to show how you can do pairwise comparisons. You can customize this to your dataset.
```
# PacBio vs. Gencode
python ./00_scripts/17_protein_groups_compare.py \
--pg_fileOne ./16_MetaMorpheus/AllQuantifiedProteinGroups.Gencode.tsv \
--pg_fileTwo ./16_MetaMorpheus/AllQuantifiedProteinGroups.jurkat.hybrid.tsv \
--mapping ./15_accession_mapping/accession_map_gencode_uniprot_pacbio.tsv \
--output ./17_protein_group_comparison

# PacBio vs. UniProt
python ./00_scripts/17_protein_groups_compare.py \
--pg_fileOne ./16_MetaMorpheus/AllQuantifiedProteinGroups.uniprot.tsv \
--pg_fileTwo ./16_MetaMorpheus/AllQuantifiedProteinGroups.jurkat.hybrid.tsv \
--mapping ./15_accession_mapping/accession_map_gencode_uniprot_pacbio.tsv \
--output ./17_protein_group_comparison

# Gencode vs. Uniprot
python ./00_scripts/17_protein_groups_compare.py \
--pg_fileOne ./16_MetaMorpheus/AllQuantifiedProteinGroups.Gencode.tsv \
--pg_fileTwo ./16_MetaMorpheus/AllQuantifiedProteinGroups.uniprot.tsv \
--mapping ./15_accession_mapping/accession_map_gencode_uniprot_pacbio.tsv \
--output ./17_protein_group_comparison

conda deactivate
```

## Proceed to
