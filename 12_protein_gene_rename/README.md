# Protein Gene Rename 
Mapings of PacBio transcripts/proteins to GENCODE genes. Some PacBio transcripts and the associated PacBio predicted protein can map two different genes. Some transcripts can also map to multiple genes. <br />

_Input:_ <br />
- cds.gtf (from [07 Make CDS GTF module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_make_cds_gtf))
- orf_refined.fasta (from [06 Refine ORF Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_refine_orf_database))
- orf_refined.tsv (from [06 Refine ORF Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_refine_orf_database))
- genes.tsv (from [11 Protein Classification module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/11_protein_classification))
  
_Output:_
- orf_refined_gene_update.tsv
- cds_refined.gtf
- protein_refined.fasta

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
Run the script. I am not purging the modules or deactivating the environment, becuase they are needed for the next modules.
```
python ./00_scripts/12_protein_gene_rename.py \
    --sample_gtf ./07_make_cds_gtf/jurkat_with_cds.gtf \
    --sample_protein_fasta ./06_refine_orf_database/jurkat_orf_refined.fasta \
    --sample_refined_info ./06_refine_orf_database/jurkat_orf_refined.tsv \
    --pb_protein_genes ./11_protein_classification/jurkat_genes.tsv \
    --name ./12_protein_gene_rename/jurkat
```

## Proceed to [13 Protein Filter module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/13_protein_filter)
