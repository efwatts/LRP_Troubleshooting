# Open Reading Frame (ORF) Calling
The python script in this repository finds the best ORFs (after CPAT lists all possible ORFs) <br />
The script MUST be run using a Docker (as of February 2024) for now <br />
The docker is outdated and won't run locally on Docker <br />
It can run in Apptainer (the replacement for Singularity) on Rivanna, the UVA HPC <br />

_Input:_ <br />
- ORF_prob.tsv (from [03_CPAT module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_CPAT))
- ORF_seqs.fa (from [03_CPAT module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_CPAT))
- annotated_genome.gtf (from [Gencode](https://www.gencodegenes.org/))
- corrected.gtf (from [02_SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_SQANTI))
- pb_gene.tsv (from [03_transcriptome_summary module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_transcriptome_summary))
- classification.txt (from [02_SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_SQANTI))
- corrected.fasta (from [02_SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_SQANTI))

_Output:_
- all_orfs_mapped.tsv
- best_ORF.tsv

## Next go to Refine module
