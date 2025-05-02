# Open Reading Frame (ORF) Calling
This module is used to call the best open reading frames (ORFs) using the following filters after CPAT: <br />
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
Here is an AI generated summary of this step: <br />
> The `orf_calling.py` script is designed to identify and classify open reading frames (ORFs) from RNA sequences. It takes as input ORF coordinates, ORF sequences, a GENCODE annotation file, a sample GTF file, a PB gene file, a classification file, and a sample FASTA file. The script processes the input data to identify the best ORF for each transcript based on various criteria, including coding probability scores and upstream ATG counts. It generates output files containing the best ORFs and their classifications.

The script MUST be run using a Docker, because of python compatibility issues (as of April 2024) <br />
The Docker can run in Apptainer (the replacement for Singularity) on Rivanna, the UVA HPC <br />
*** The format of the ID inputs matter. The original script is written for PacBio accession numbers ***

## Input files
- `ORF_prob.tsv` - CPAT output file with ORF coordinates and coding probability scores
- `ORF_seqs.fa` - CPAT output file with ORF sequences
- `annotated_genome.gtf` - GENCODE annotation file
- `filtered_corrected.gtf` - SQANTI3 filtered GTF file
- `pb_gene.tsv` - PB gene file from SQANTI3
- `classification.5degfilter.tsv` - SQANTI3 filtered classification file
- `filtered_corrected.fasta` - SQANTI3 filtered FASTA file

## Required installations
Load modules (if on HPC) and create and activate conda environment. <br />
```
module load apptainer/1.3.4
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda env create -f 00_environments/05_orf_calling.yml
conda activate orf-calling
```
Load Docker (here using Apptainer). <br />
```
apptainer pull docker://gsheynkmanlab/orf_calling:latest
```
## Run ORF calling from a SLURM script <br />
```
sbatch 00_scripts/05_orf_calling.sh
```
## Or run these commands. <br />
Note, this is where the docker image lives on the Sheynkman lab server. If you are using a different server, you will need to change the path to the docker image. <br />```
```
apptainer exec /project/sheynkman/dockers/LRP/orf_calling_latest.sif /bin/bash -c "\
    python 00_scripts/05_orf_calling_multisample.py \
    --orf_coord 04_CPAT/sample.ORF_prob.tsv \
    --orf_fasta 04_CPAT/sample.ORF_seqs.fa \
    --gencode /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
    --sample_gtf 03_filter_sqanti/sample_corrected.5degfilter.gff \
    --pb_gene 04_transcriptome_summary/pb_gene.tsv \
    --classification 03_filter_sqanti/sample_classification.5degfilter.tsv \
    --sample_fasta 03_filter_sqanti/sample_corrected.5degfilter.fasta \
    --output_mutant 05_orf_calling/best_ORF_condition1.tsv \
    --output_wt 05_orf_calling/best_ORF_condition2.tsv
"

conda deactivate
module purge
```
## Proceed to [06_refine_orf_database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_refine_orf_database)
