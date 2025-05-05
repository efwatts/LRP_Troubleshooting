# Make Hybrid Database 
Makes a hybrid database that is composed of high-confidence PacBio proteins and GENCODE proteins for genes that are not in the high-confidence space. <br />

High-confidence is defined as genes in which the PacBio sampling is adequate (default average transcript length 1-4kb) and a total of 3 CPM (counts per million; default) per gene <br />
Here is an AI generated summary of this step: <br />
> The `make_hybrid_database.py` script is designed to create a hybrid protein database by combining high-confidence PacBio proteins with GENCODE proteins. It takes as input several files, including a protein classification file, gene length information, filtered protein sequences, GENCODE clusters, refined gene information, and a filtered GTF file. The script processes these inputs to generate a hybrid database that includes high-confidence genes and their corresponding protein sequences. The output files include a GTF file with high-confidence CDS annotations, a TSV file with high-confidence gene information, a FASTA file with hybrid protein sequences, and a refined high-confidence TSV file.
## Input files
- `classification_filtered.tsv` - protein classification file from the [13 Protein Filter module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/13_protein_filter)
- `gene_lens.tsv` - gene length information from the [01 Reference Tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables)
- `filtered_protein.fasta` - filtered protein sequences from the [13 Protein Filter module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/13_protein_filter)
- `gencode_clusters.fasta` - GENCODE clusters from the [02 Make Gencode Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_make_gencode_database)
- `orf_refined_gene_update.tsv` - refined gene information from the [12 Protein Gene Rename module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/12_protein_gene_rename)
- `cds_filtered.gtf` - filtered GTF file from the [13 Protein Filter module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/13_protein_filter)
## Required installations
If you kept your modules and environment loaded from the last module, you can skip this step. <br />
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda activate protein_class
```
## Run Hybrid Database from a SLURM script
```
sbatch 00_scripts/14_make_hybrid_database.sh
```
## Or run these commands.
```
# Condition 1
python ./00_scripts/14_make_hybrid_database.py \
    --protein_classification 13_protein_filter/condition1.classification_filtered.tsv \
    --gene_lens 01_reference_tables/gene_lens.tsv \
    --pb_fasta 13_protein_filter/condition1.filtered_protein.fasta \
    --gc_fasta 02_make_gencode_database/gencode_clusters.fasta \
    --refined_info 12_protein_gene_rename/condition1_orf_refined_gene_update.tsv \
    --pb_cds_gtf 13_protein_filter/condition1_with_cds_filtered.gtf \
    --name 14_protein_hybrid_database/condition1

# Condition 2
python ./00_scripts/14_make_hybrid_database.py \
    --protein_classification 13_protein_filter/condition2.classification_filtered.tsv \
    --gene_lens 01_reference_tables/gene_lens.tsv \
    --pb_fasta 13_protein_filter/condition2.filtered_protein.fasta \
    --gc_fasta 02_make_gencode_database/gencode_clusters.fasta \
    --refined_info 12_protein_gene_rename/condition2_orf_refined_gene_update.tsv \
    --pb_cds_gtf 13_protein_filter/condition2_with_cds_filtered.gtf \
    --name 14_protein_hybrid_database/condition2

conda deactivate
module purge
```
## Change the defaults
If you want to change the defaults for high confidence, you can use the `--lower_kb` and `--upper_kb` flags to set the lower and upper bounds for the average transcript length, respectively. You can also use the `--lower_cpm` flag to set the minimum CPM threshold for high-confidence genes. <br />
```
python 00_scripts/14_make_hybrid_database.py \
    --protein_classification 13_protein_filter/classification_filtered.tsv \
    --gene_lens 01_reference_tables/gene_lens.tsv \
    --pb_fasta 13_protein_filter/filtered_protein.fasta \
    --gc_fasta 02_make_gencode_database/gencode_clusters.fasta \
    --refined_info 12_protein_gene_rename/orf_refined_gene_update.tsv \
    --pb_cds_gtf 13_protein_filter/jurkat_with_cds_filtered.gtf \
    --name 14_protein_hybrid_database/sample \
    --lower_kb ${params.lower_kb} \
    --upper_kb ${params.upper_kb} \
    --lower_cpm ${params.lower_cpm}
```

## Proceed to [15 MS File Conversion module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/15_MS_file_convert) if you have MS data.
## Or proceed to [17 Track Visualization module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/17_track_visualization) if you do not have MS data (most cases).