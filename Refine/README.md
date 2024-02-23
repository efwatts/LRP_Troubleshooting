# Refine ORFs 
This module filters the ORFs fro ORF calling to only include accessions with CPAT coding score above a threshold (default 0.0). <br />
It also filters to include only ORFs with a stop codon and collapses transcripts that produce the same protein. <br />

_Input:_ 
- best_ORFs.tsv (from orf-calling)
- corrected.fasta (from SQANTI3)

_Output:_ 
- orf_refined.tsv
- orf_refined.fasta
