# Accession Mapping
Maps protein entries within GENCODE, UniProt and PacBio databases to one another based on sequence similarity

_Input:_ <br />
- gene_isoname.tsv (from [01 Reference Tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))
- gencode_clusters.fasta (from [02 Make Gencode Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_make_gencode_database))
- orf_refined.fasta (from [06 Refine ORF Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_refine_orf_database)) (this could also be substituted with the hybrid database from [14 Make Hybrid Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/14_make_hybrid_database) or [13 Protein Filter module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/13_protein_filter), depending on the databases you want to compare)
- uniprot.fasta (from [UniProt](https://www.uniprot.org/help/downloads))
  
_Output:_
- accession_map_genocde_uniprot_pacbio.tsv
- accession_map_stats.tsv

## Run script
If running on Rivanna or other HPC, load required modules. Use the reference tables environment from [01 Reference Tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables).
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11

conda activate reference_tab
```
Run the script.
```
python ./00_scripts/15_accession_mapping.py \
--gencode_fasta ./02_make_gencode_database/gencode_clusters.fasta \
--pacbio_fasta ./06_refine_orf_database/jurkat_orf_refined.fasta \
--uniprot_fasta ./00_input_data/uniprot_reviewed_canonical_and_isoform.fasta

conda deactivate
```

## Proceed to 
