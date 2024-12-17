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
  
This module consists of two scripts that build on each other. 

_Input:_ <br />
- protein_classification_w_5utr_info.tsv (from [10 5 Prime UTR module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/10_5p_utr))
- best_orf.tsv (from [05 ORF Calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling))
- orf_refined.tsv (from [06 Refine ORF Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_refine_orf_database))
- ensg_gene.tsv (from [01 Reference Tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))
  
_Output:_
- genes.tsv
- protein_classification_w_meta.tsv
- protein_classification.tsv

## Run scripts
If running on Rivanna or other HPC, load required modules.
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load miniforge/24.3.0-py3.11
```
I created a conda environment, because there was no .yml file. I will make one in the future
```
conda create -n protein_class
conda activate protein_class
conda install pandas argparse
```
Run the scripts. I am not purging the modules or deactivating the environment, becuase they are needed for the next modules.
```
python ./00_scripts/11_protein_classification_add_meta.py \
--protein_classification  ./10_5p_utr/jurkat.sqanti_protein_classification_w_5utr_info.tsv \
--best_orf ./05_orf_calling/jurkat_best_orf.tsv \
--refined_meta ./04_refine_orf_database/jurkat_orf_refined.tsv \
--ensg_gene ./01_reference_tables/ensg_gene.tsv \
--name jurkat \
--dest_dir ./11_protein_classification/


python ./00_scripts/11_protein_classification.py \
--sqanti_protein ./11_protein_classification/jurkat.protein_classification_w_meta.tsv \
--name jurkat \
--dest_dir ./11_protein_classification/
```

## Proceed to [12 Protein Gene Rename module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/12_protein_gene_rename)
