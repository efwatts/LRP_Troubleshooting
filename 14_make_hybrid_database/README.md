# Protein Filter 
Makes a hybrid database that is composed of high-confidence PacBio proteins and GENCODE proteins for genes that are not in the high-confidence space. <br />

High-confidence is defined as genes in which the PacBio sampling is adequate (default average transcript length 1-4kb) and a total of 3 CPM (counts per million; default) per gene <br />

_Input:_ <br />
- classification_filtered.tsv (from [13 Protein Filter module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/13_protein_filter))
- gene_lens.tsv (from [01 Reference Tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))
- filtered_protein.fasta (from [13 Protein Filter module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/13_protein_filter))
- gencode_clusters.fasta (from [02 Make Gencode Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_make_gencode_database))
- orf_refined_gene_update.tsv (from [12 Protein Gene Rename module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/12_protein_gene_rename))
- cds_filtered.gtf (from [13 Protein Filter module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/13_protein_filter))
  
_Output:_
- cds_high_confidence.gtf
- high_confidence_genes.tsv
- hybrid.fasta
- refined_high_confidence.tsv

## Run script
If running on Rivanna or other HPC, load required modules. If you kept your modules and environment loaded from the last module, you can skip this step.
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11

conda activate protein_class
```
Run the script. 
```
python ./00_scripts/14_make_hybrid_database.py \
    --protein_classification ./13_protein_filter/jurkat.classification_filtered.tsv \
    --gene_lens ./01_reference_tables/gene_lens.tsv \
    --pb_fasta ./13_protein_filter/jurkat.filtered_protein.fasta \
    --gc_fasta ./02_make_gencode_database/gencode_clusters.fasta \
    --refined_info ./12_protein_gene_rename/jurkat_orf_refined_gene_update.tsv \
    --pb_cds_gtf ./13_protein_filter/jurkat_with_cds_filtered.gtf \
    --name ./14_protein_hybrid_database/jurkat

conda deactivate
```
You can change the defaults for high confidence by adding the arguments below.
```
python ./00_scripts/14_make_hybrid_database.py \
    --protein_classification ./13_protein_filter/jurkat.classification_filtered.tsv \
    --gene_lens ./01_reference_tables/gene_lens.tsv \
    --pb_fasta ./13_protein_filter/jurkat.filtered_protein.fasta \
    --gc_fasta ./02_make_gencode_database/gencode_clusters.fasta \
    --refined_info ./12_protein_gene_rename/jurkat_orf_refined_gene_update.tsv \
    --pb_cds_gtf ./13_protein_filter/jurkat_with_cds_filtered.gtf \
    --name ./14_protein_hybrid_database/jurkat \
    --lower_kb ${params.lower_kb} \
    --upper_kb ${params.upper_kb} \
    --lower_cpm ${params.lower_cpm}
```

## Proceed to [14 Make Hybrid Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/14_make_hybrid_database)
