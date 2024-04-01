# Long Read Transcriptome Summary <br />
Compile data for downstream analyses. <br />
_Input_
- --sq_out	classification.txt file (from [02_SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_SQANTI))
- --tpm	Kallisto TPM file location	
- --ribo	Normalized Kallisto Ribodepletion TPM file location	
- --ensg_to_gene	ENSG -> Gene Map file location (from [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))
- --enst_to_isoname	ENST -> Isoname Map file location	(from [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))
- --len_stats	Gene Length Statistics table location (from [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))

_Output_
- gene_level_tab.tsv	gene level table	
- sqanti_isoform_info.tsv	sqanti isoform table

** I'm not sure how to get the Kallisto files, so skipping for now **

## 
