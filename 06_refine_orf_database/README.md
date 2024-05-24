# Refine ORF Database
Refine the database of ORFs created in the [05 ORF-calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling) based on a user-assigned threshold.<br />
- Filters ORF database to only include accessions with a CPAT coding score above a threshold (default 0.0)
- Filters ORFs to only include ORFs that have a stop codon
- Collapses transcripts that produce the same protein into one entry, keeping a base accession (first alphanumeric).
- Abundances of transcripts (CPM) are collapsed during this process.

_Input:_ <br />
- User-assigned name, based on sample and cutoff threshold
- best_ORF.tsv (from [05 ORF-calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling)) 
- filtered_corrected.fasta (from [03_filter_sqanti module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti))
- Coding score cutoff assigned by user (in decimal form)

_Output:_
- orf_refined.fasta
- orf_refined.tsv

## Run ORF calling
First, build a conda environment and load modules (if using Rivanna or other HPC). <br />
```
module load apptainer/1.2.2
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10

conda env create -f ./00_environments/06_refine_orf_database.yml
conda activate refined-database-generation
```
Then enter the apptainer and call the python script either using `06_refine_orf_database.sh` or the following command: <br />
```
python ./00_scripts/06_refine_orf_database.py \
--name ./06_refine_orf_database/jurkat_30 \
--orfs ./05_orf_calling/jurkat_best_ORF.tsv \
--pb_fasta ./03_filter_sqanti/filtered_jurkat_corrected.fasta \
--coding_score_cutoff 0.3 

conda deactivate 
```
## Proceed to [07_make_cds_gtf module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_make_cds_gtf)
