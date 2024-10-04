# Open Reading Frame (ORF) Calling
The python script in this repository finds the best ORFs (after CPAT lists all possible ORFs) <br />
- Selects the most plausible ORF from each pacbio transcript, using the following information
  - comparison of ATG start to reference (GENCODE)
    - selects ORF with ATG start matching the one in the reference, if it exists
  - coding probability score from CPAT
  - number of upstream ATGs for the candidate ORF
    - decrease score as number of upstream ATGs increases using sigmoid function
- Additionally provides calling confidence of each ORF called
  - Clear Best ORF : best score and fewest upstream ATGs of all called ORFs
  - Plausible ORF : not clear best, but decent CPAT coding_score (>0.364)
  - Low Quality ORF : low CPAT coding_score (<0.364)

The script MUST be run using a Docker, because of python compatibility issues (as of April 2024) <br />
The Docker can run in Apptainer (the replacement for Singularity) on Rivanna, the UVA HPC <br />
*** The format of the ID inputs matter. The original script is written for PacBio accession numbers. I have provided alternative scripts for Mandalorian and Bambu and will update for more as I use them. ***

_Input:_ <br />
- ORF_prob.tsv (from [04_CPAT module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_CPAT))
- ORF_seqs.fa (from [04_CPAT module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_CPAT))
- annotated_genome.gtf (from [Gencode](https://www.gencodegenes.org/))
- filtered_corrected.gtf (from [03_filter_sqanti module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti))
- pb_gene.tsv (from [03_transcriptome_summary module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_transcriptome_summary))
- filtered_classification.tsv (from [03_filter_sqanti module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti))
- filtered_corrected.fasta (from [03_filter_sqanti module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti))

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

conda env create -f ./00_environments/05_orf_calling.yml
conda activate orf-calling
```
Add the apptainer to the scratch folder before entering the apptainer and make sure that your working directory is in scratch so you can write output files.
```
apptainer exec --bind $SCRATCH:/project/sheynkman/users/emily/LRP_test/jurkat orf_calling_latest.sif ls /project/sheynkman/users/emily/LRP_test/jurkat
apptainer exec orf_calling_latest.sif ls $SCRATCH
```
Then enter the apptainer and call the python script either using `05_orf_calling.sh` or the following command: <br />
```
python ./00_scripts/05_orf_calling.py \
--orf_coord ./04_CPAT/cpat.ORF_prob.tsv \
--orf_fasta ./04_CPAT/cpat.ORF_seqs.fa \
--gencode ./00_input_data/gencode.v35.annotation.canonical.gtf \
--sample_gtf ./03_filter_sqanti/filtered_jurkat_corrected.gtf \
--pb_gene ./04_transcriptome_summary/pb_gene.tsv \
--classification ./03_filter_sqanti/filtered_jurkat_classification.tsv \
--sample_fasta ./03_filter_sqanti/filtered_jurkat_corrected.fasta \
--output ./05_orf_calling/jurkat_best_ORF.tsv

exit

conda deactivate
```
## Proceed to [06_refine_orf_database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_refine_orf_database)
