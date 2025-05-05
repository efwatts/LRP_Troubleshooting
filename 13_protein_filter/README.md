# Protein Filter 
Filters out proteins that are:
- not pFSM, pNIC, pNNC
- are pISMs (either N-terminus or C-terminus truncations)
- pNNC with junctions after the stop codon (default 2) <br />
Here is an AI generated summary of this step: <br />
> The `protein_filter.py` script is designed to filter protein sequences based on specific criteria. It takes as input a protein classification file, a GTF file containing gene annotations, and a FASTA file with protein sequences. The script filters out proteins that do not meet the specified criteria, such as being classified as pFSM, pNIC, or pNNC. Additionally, it removes proteins that are classified as pISMs (either N-terminus or C-terminus truncations) and those that have junctions after the stop codon. The output includes filtered protein sequences and a summary of the filtering process.
## Input files
- `protein_classification.tsv` - protein classification file from the [11 Protein Classification module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/11_protein_classification)
- `gencode.annotation.gtf` - GTF file containing gene annotations from Gencode
- `protein_refined.fasta` - FASTA file with protein sequences from the [12 Protein Gene Rename module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/12_protein_gene_rename)
- `cds_refined.gtf` - GTF file with refined CDS annotations from the [12 Protein Gene Rename module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/12_protein_gene_rename)
## Required installations
Load modules (if on HPC) and activate conda environment. <br />
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda activate protein_class
```
## Run Protein Filter from a SLURM script
```
sbatch 00_scripts/13_protein_filter.sh
```
## Or run these commands.
```
# condition 1
python 00_scripts/13_protein_filter.py \
--protein_classification 11_protein_classification/condition1.protein_classification.tsv \
--gencode_gtf /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
--protein_fasta 12_protein_gene_rename/condition1.protein_refined.fasta \
--sample_cds_gtf 12_protein_gene_rename/condition1_with_cds_refined.gtf \
--min_junctions_after_stop_codon 2 \
--name 13_protein_filter/condition1

# condition 2
python 00_scripts/13_protein_filter.py \
--protein_classification 11_protein_classification/condition2.protein_classification.tsv \
--gencode_gtf /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
--protein_fasta 12_protein_gene_rename/condition2.protein_refined.fasta \
--sample_cds_gtf 12_protein_gene_rename/condition2_with_cds_refined.gtf \
--min_junctions_after_stop_codon 2 \
--name 13_protein_filter/condition2

conda deactivate
module purge
```

## Proceed to [14 Make Hybrid Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/14_make_hybrid_database)
