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

## Run ORF calling
First, build a conda environment and load modules (if using Rivanna or other HPC). <br />
```
module load gcc/11.4.0
module load mamba/22.11.1-4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11
module load openmpi/4.1.4
module load python/3.11.4

conda env create -f ./00_environments/transcriptome_sum.yml
conda activate transcriptome_sum
```
Then call the python script either using `03_transcriptome_summary.sh` or the following command: <br />
```
python ./00_scripts/03_transcriptome_summary.py \
--sq_out ./02_sqanti/output/jurkat_classification.txt \
--tpm ./00_input_data/jurkat_gene_kallisto.tsv \
--ribo ./00_input_data/kallist_table_rdeplete_jurkat.tsv \
--ensg_to_gene ./01_reference_tables/ensg_gene.tsv \
--enst_to_isoname ./01_reference_tables/enst_isoname.tsv \
--len_stats ./01_reference_tables/gene_lens.tsv \
--odir ./03_transcriptome_summary/

conda deactivate
```
## Proceed to Refine module
