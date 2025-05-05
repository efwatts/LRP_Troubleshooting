# Protein Classification 
Classifies proteins based on their splicing and start sites. <br />

The main classifications are the following: <br />
- pFSM: full-protein-match
  - protein fully matches a gencode protein
- pISM: incomplete-protein-match
  - protein only partially matches gencode protein
  - considered an N- or C-terminus truncation artifact
- pNIC: novel-in-catelog
  - protein composed of known N-term, splicing, and/or C-term in new combinations
- pNNC: novel-not-in-catelog
  - protein composed of novel N-term, splicing, and/or C-terminus
  
This module consists of two scripts that build on each other. <br />
Here is an AI generated summary of this step: <br />
> The `protein_classification.py` script is designed to classify proteins based on their coding potential and structural features. It takes as input a GTF file containing transcript annotations, a GTF file with CDS regions, an ORF database, and a reference GTF file. The script processes these inputs to generate a protein classification report, which includes information about the coding potential of the transcripts, their structural features, and their alignment to the reference genome. The resulting report can be used for downstream analysis in RNA-seq studies, particularly in the context of proteomics and functional genomics.
## Input files
- `condition1.sqanti_protein_classification_w_5utr_info.tsv` - protein classification file from the [10_5p_utr module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/10_5p_utr)
- `condition1_best_orf.tsv` - ORF database from the [05_orf_calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling)
- `condition1_orf_refined.tsv` - refined ORF database from the [06_refine_orf_database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_refine_orf_database)
- `condition2.sqanti_protein_classification_w_5utr_info.tsv` - protein classification file from the [10_5p_utr module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/10_5p_utr)
- `condition2_best_orf.tsv` - ORF database from the [05_orf_calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling)
- `condition2_orf_refined.tsv` - refined ORF database from the [06_refine_orf_database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_refine_orf_database)
- `ensg_gene.tsv` - ENSEMBL gene file from the [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables)

## Required installations
Load modules (if on HPC) and create and activate `protein_classification` conda environment. <br />
```
module load gcc/11.4.0
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda env create -f ./00_environments/11_protein_class.yml
conda activate protein_class
```
## Run protein classification from a SLURM script
```
sbatch 00_scripts/11_protein_classification.sh
```
## Or run these commands.
```
# condition 1
python 00_scripts/11_protein_classification_add_meta.py \
--protein_classification  10_5p_utr/condition1.sqanti_protein_classification_w_5utr_info.tsv \
--best_orf 05_orf_calling/best_ORF_condition1.tsv \
--refined_meta 06_refine_orf_database/condition1_0_orf_refined.tsv \
--ensg_gene 01_reference_tables/ensg_gene.tsv \
--name condition1 \
--dest_dir 11_protein_classification/

python 00_scripts/11_protein_classification.py \
--sqanti_protein 11_protein_classification/condition1.protein_classification_w_meta.tsv \
--name condition1 \
--dest_dir 11_protein_classification/

# condition 2
python 00_scripts/11_protein_classification_add_meta.py \
--protein_classification  10_5p_utr/condition2.sqanti_protein_classification_w_5utr_info.tsv \
--best_orf 05_orf_calling/best_ORF_condition2.tsv \
--refined_meta 06_refine_orf_database/condition2_0_orf_refined.tsv \
--ensg_gene 01_reference_tables/ensg_gene.tsv \
--name condition2 \
--dest_dir 11_protein_classification/

python 00_scripts/11_protein_classification.py \
--sqanti_protein 11_protein_classification/condition2.protein_classification_w_meta.tsv \
--name condition2 \
--dest_dir 11_protein_classification/

conda deactivate 
module purge
```
## Proceed to [12 Protein Gene Rename module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/12_protein_gene_rename)
