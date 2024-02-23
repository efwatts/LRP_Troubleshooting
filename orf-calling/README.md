# Open Reading Frame (ORF) Calling
The python script in this repository finds the best ORFs (after CPAT lists all possible ORFs) <br />
The script MUST be run using a Docker (as of February 2024) for now <br />
The docker is outdated and won't run locally on Docker <br />
It can run in Apptainer (the replacement for Singularity) on Rivanna, the UVA HPC <br />

_Input:_ <br />
- ORF_prob.tsv (from CPAT)
- ORF_seqs.fa (from CPAT
- annotated_genome.gtf
- corrected.gtf (from SQANTI3)
- pb_gene.tsv
- classification.txt (from Iso-Seq...I think)
- corrected.fasta (from SQANTI3)

_Output:_
- all_orfs_mapped.tsv
- best_ORF.tsv
