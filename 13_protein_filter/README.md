# Protein Filter 
Filters out proteins that are:
- not pFSM, pNIC, pNNC
- are pISMs (either N-terminus or C-terminus truncations)
- pNNC with junctions after the stop codon (default 2) <br />

_Input:_ <br />
- protein_classification.tsv (from [11 Protein Classification module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/11_protein_classification))
- gencode.annotation.gtf (from [Gencode](https://www.gencodegenes.org/))
- protein_refined.fasta (from [12 Protein Gene Rename module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/12_protein_gene_rename))
- cds_refined.gtf (from [12 Protein Gene Rename module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/12_protein_gene_rename))
  
_Output:_
- class_info.tsv
- cds_filtered.gtf
- classification_filtered.tsv
- filtered_protein.fasta

## Run script
If running on Rivanna or other HPC, load required modules. If you kept your modules and environment loaded from the last module, you can skip this step.
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load miniforge/24.3.0-py3.11

conda activate protein_class
```
Run the script. You need to set the minimum junctions after stop coding. Now it is set to 2. <br />
I am not purging the modules or deactivating the environment, becuase they are needed for the next modules.
```
python ./00_scripts/13_protein_filter.py \
--protein_classification ./11_protein_classification/jurkat.protein_classification.tsv \
--gencode_gtf ./00_input_data/gencode.v35.annotation.canonical.gtf \
--protein_fasta ./12_protein_gene_rename/jurkat.protein_refined.fasta \
--sample_cds_gtf ./12_protein_gene_rename/jurkat_with_cds_refined.gtf \
--min_junctions_after_stop_codon 2 \
--name ./13_protein_filter/jurkat
```

## Proceed to [14 Make Hybrid Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/14_make_hybrid_database)
