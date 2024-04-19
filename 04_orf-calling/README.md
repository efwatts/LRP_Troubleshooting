# Open Reading Frame (ORF) Calling
The python script in this repository finds the best ORFs (after CPAT lists all possible ORFs) <br />
The script MUST be run using a Docker, because of python compatibility issues (as of April 2024) <br />
The Docker can run in Apptainer (the replacement for Singularity) on Rivanna, the UVA HPC <br />

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
First, build a conda environment, load docker, and load modules (if using Rivanna or other HPC). <br />
```
module load apptainer/1.2.2
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10

apptainer pull docker://gsheynkmanlab/orf_calling:latest

conda env create -f ./00_environments/orf_calling.yml
conda activate orf-calling
```
Add the apptainer to the scratch folder before entering the apptainer and make sure that your working directory is in scratch so you can write output files.
```
apptainer exec --bind $SCRATCH:/project/sheynkman/users/emily/LRP_test/jurkat orf_calling_latest.sif ls /project/sheynkman/users/emily/LRP_test/jurkat
apptainer exec orf_calling_latest.sif ls $SCRATCH
```
Then enter the apptainer and call the python script either using `04_orf_calling.sh` or the following command: <br />
```
python ./00_scripts/04_orf_calling.py \
--orf_coord ./03_CPAT/cpat.ORF_prob.tsv \
--orf_fasta ./03_CPAT/cpat.ORF_seqs.fa \
--gencode ./00_input_data/gencode.v35.annotation.canonical.gtf \
--sample_gtf ./02_sqanti/output/jurkat_corrected.gtf \
--pb_gene ./03_transcriptome_summary/pb_gene.tsv \
--classification ./02_sqanti/output/jurkat_classification.txt \
--sample_fasta ./02_sqanti/output/jurkat_corrected.fasta \
--output ./04_orf_calling/jurkat_best_ORF.tsv

exit

conda deactivate
```
## Proceed to [Refine ORF Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_refine_orf_database)
