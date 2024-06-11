# Peptide Analysis 
Generate a table comparing MS peptide results between the PacBio and GENCODE databases.

_Input:_ <br />
- gene_isoname.tsv (from [01 Reference Tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))
- AllPeptides.Gencode.psmtsv (from [16 MetaMorpheus module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/16_MetaMorpheus))
- orf_refined.fasta (from [06 Refined ORF Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_refine_orf_database))
- filtered_protein.fasta (from [13 Protein Filter module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/13_protein_filter))
- hybrid.fasta (from [14 Make Hybrid Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/14_make_hybrid_database))
- pb_gene.tsv (from [04 Transcriptome Summary module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_transcriptome_summary))
  
_Output:_
- gc_pb_overlap_peptides.tsv

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
python ./00_scripts/17_peptide_analysis.py \
	--gene_to_isoname ./00_test_data/gene_isoname.tsv \
	--gencode_peptides ./16_MetaMorpheus/gencode/Task1SearchTask/AllPeptides.psmtsv \
	--pb_refined_fasta ./00_test_data/jurkat_orf_refined.fasta \
	--pb_filtered_fasta ./12_protein_filter/jurkat.filtered_protein.fasta \
	--pb_hybrid_fasta ./13_protein_hybrid_database/jurkat_hybrid.fasta \
	--pb_gene ./03_transcriptome_summary/pb_gene.tsv \
	--output_directory ./17_peptide_analysis
```

## Proceed to 
