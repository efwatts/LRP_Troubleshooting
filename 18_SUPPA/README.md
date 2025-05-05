# Run SUPPA to identify alternative splice sites
Run the tool from the [Computational RNA Biology group](https://github.com/comprna), [SUPPA](https://github.com/comprna/SUPPA). <br />

Here is an AI generated summary of what SUPPA is: <br />
> SUPPA is a computational tool designed for the analysis of alternative splicing events in RNA-Seq data. It allows researchers to identify and quantify different types of splicing events, such as skipped exons, mutually exclusive exons, and retained introns. SUPPA uses a probabilistic model to estimate the inclusion levels of alternative exons and provides various output formats for downstream analysis. The tool is particularly useful for studying gene expression regulation and the functional consequences of alternative splicing in different biological contexts.
## Input files
- `sample_corrected.5degfilter.gff` - GFF file with corrected 5' and 3' ends for each sample. This file is generated from the [03 Filter SQANTI](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti) module.
## Required installations
Load modules (if on HPC) and create and activate conda environment. <br />
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11
module load R/4.4.1

conda env create -f 00_environments/suppa.yml
conda activate suppa
```
## Run SUPPA from a SLURM script
```
sbatch 00_scripts/18_suppa.sh
```
## Or run these commands.
Note: there is some manual file manipulation in this step. I plant to edit the original scripts to do this automatically in the future. <br />
```
#Generate splicing events. 
python /project/sheynkman/programs/SUPPA-2.4/suppa.py generateEvents -i 03_filter_sqanti/sample_corrected.5degfilter.gff -o 18_SUPPA/01_splice_events/all.events -e SE SS MX RI FL -f ioe

#Put all IOE events in the same file.
cd 18_SUPPA/01_splice_events

awk '
    FNR==1 && NR!=1 { while (/^<header>/) getline; }
    1 {print}
' *.ioe > all.events.ioe

cd ../../..

#Create expression table.
python 00_scripts/18_expression_table.py 03_filter_sqanti/sample_classification.5degfilter.tsv 18_SUPPA/expression_table.tsv

#Must remove first title column from expression table

#Calculate PSI values.
python /project/sheynkman/programs/SUPPA-2.4/suppa.py psiPerEvent --ioe-file 18_SUPPA/01_splice_events/all.events.ioe --expression-file 18_SUPPA/expression_table.tsv -o 18_SUPPA/combined_local

#Differential splicing. Split the PSI and TPM files between the two conditions (if comparing)
Rscript 00_scripts/18_suppa_split_file.R 18_SUPPA/expression_table.tsv BioSample_1,BioSample_2,BioSample_3 BioSample_4,BioSample_5,BioSample_6 18_SUPPA/condition1.tpm 18_SUPPA/condition2.tpm -i
Rscript 00_scripts/18_suppa_split_file.R 18_SUPPA/combined_local.psi BioSample_1,BioSample_2,BioSample_3 BioSample_4,BioSample_5,BioSample_6 18_SUPPA/condition1.psi 18_SUPPA/condition2.psi -e

#Analyze differential splicing.
python /project/sheynkman/programs/SUPPA-2.4/suppa.py diffSplice \
    -m empirical \
    -i 18_SUPPA/01_splice_events/all.events.ioe \
    -p 18_SUPPA/condition1.psi 18_SUPPA/condition2.psi \
    -e 18_SUPPA/condition1.tpm 18_SUPPA/condition2.tpm \
    -gc \
    -o 18_SUPPA/FBS_diffsplice

conda deactivate
module purge
```
## Proceed to [19 LRP Summary](https://github.com/efwatts/LRP_Troubleshooting/tree/main/19_LRP_summary)