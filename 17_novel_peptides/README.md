# Novel Peptides
Finds novel peptides between sample database and GENCODE. Novel peptide is defined as a peptide found in PacBio (refined, filtered, and hybrid) that could not be found in GENCODE or UniProt.

_Input:_ <br />
- AllQuantifiedProteinGroups.sample.tsv (refined, hybrid, and filtered) (from [16 MetaMorpheus module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/16_MetaMorpheus))
- gencode_clusters.fasta (from [02 Make Gencode Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_make_gencode_database))
- uniprot.fasta (from [UniProt](https://www.uniprot.org/help/downloads))
  
_Output:_
- pacbio_novel_peptides.tsv
- pacbio_novel_peptides_to_gencode.tsv
- pacbio_novel_peptides_to_uniprot.tsv

## Run script
Call the script `17_novel_peptides.sh` with `sbatch ./00_scripts/17_novel_peptides.sh` or follow the steps below. <br />
If running on Rivanna or other HPC, load required modules. Use the reference tables environment from [01 Reference Tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables).
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11

conda activate reference_tab

# Refined
python ./00_scripts/17_novel_peptides.py \
--pacbio_peptides ./16_MetaMorpheus/AllPeptides.jurkat.refined.psmtsv \
--gencode_fasta ./02_make_gencode_database/gencode_clusters.fasta \
--uniprot_fasta ./00_input_data/uniprot_reviewed_canonical_and_isoform.fasta \
--name ./17_novel_peptides/jurkat_refined

# Filtered
python ./00_scripts/17_novel_peptides.py \
--pacbio_peptides ./16_MetaMorpheus/AllPeptides.jurkat.filtered.psmtsv \
--gencode_fasta ./02_make_gencode_database/gencode_clusters.fasta \
--uniprot_fasta ./00_input_data/uniprot_reviewed_canonical_and_isoform.fasta \
--name ./17_novel_peptides/jurkat_filtered

# Hybrid
python ./00_scripts/21_novel_peptides.py \
--pacbio_peptides ./16_MetaMorpheus/AllPeptides.jurkat.hybrid.psmtsv \
--gencode_fasta ./02_make_gencode_database/gencode_clusters.fasta \
--uniprot_fasta ./00_input_data/uniprot_reviewed_canonical_and_isoform.fasta \
--name ./17_novel_peptides/jurkat_hybrid

conda deactivate
module purge
```

## Proceed to 
