# Protein Gene Rename 
Mapings of PacBio transcripts/proteins to GENCODE genes. Some PacBio transcripts and the associated PacBio predicted protein can map two different genes. Some transcripts can also map to multiple genes. <br />
Here is an AI generated summary of this step: <br />
> The `protein_gene_rename.py` script is designed to rename protein sequences based on their corresponding gene annotations. It takes as input a GTF file containing gene annotations, a FASTA file of protein sequences, and a TSV file with refined ORF information. The script processes these inputs to generate a new GTF file with updated gene annotations, a refined FASTA file with renamed protein sequences, and a TSV file with updated ORF information. This step is important for ensuring that the protein sequences are correctly associated with their respective genes for downstream analysis.
## Input files
- `cds.gtf` - GTF file from the [07_make_cds_gtf module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_make_cds_gtf)
- `orf_refined.fasta` - FASTA file from the [06_refine_orf_database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_refine_orf_database)
- `orf_refined.tsv` - TSV file from the [06_refine_orf_database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_refine_orf_database)
- `genes.tsv` - TSV file from the [11_protein_classification module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/11_protein_classification)
## Required installations
Load modules (if on HPC) and activate conda environment. <br />
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda activate protein_class
```
## Run protein gene rename from a SLURM script
```
sbatch 00_scripts/12_protein_gene_rename.sh
```
## Or run these commands.
```
# condition 1
python ./00_scripts/12_protein_gene_rename.py \
    --sample_gtf 07_make_cds_gtf/condition1_cds.gtf \
    --sample_protein_fasta 06_refine_orf_database/condition1_0_orf_refined.fasta \
    --sample_refined_info 06_refine_orf_database/condition1_0_orf_refined.tsv \
    --pb_protein_genes 11_protein_classification/condition1_genes.tsv \
    --name 12_protein_gene_rename/condition1

# condition 2
python ./00_scripts/12_protein_gene_rename.py \
    --sample_gtf 07_make_cds_gtf/condition2_cds.gtf \
    --sample_protein_fasta 06_refine_orf_database/condition2_0_orf_refined.fasta \
    --sample_refined_info 06_refine_orf_database/condition2_0_orf_refined.tsv \
    --pb_protein_genes 11_protein_classification/condition2_genes.tsv \
    --name 12_protein_gene_rename/condition2

conda deactivate
module purge
```
## Proceed to [13 Protein Filter module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/13_protein_filter)
