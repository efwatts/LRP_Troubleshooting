# Rename CDS to exon
Make GTF input files for the next module, sqanti protein. These are basically making CDS regions look like exons. <br />

Here is an AI generated summary of this step: <br />
> The `rename_cds_to_exon_multi.py` script is designed to rename the CDS regions in a GTF file to exon regions. It takes as input a sample GTF file and a reference GTF file, and it processes these files to create new GTF files where the CDS regions are renamed to exon regions. The resulting GTF files can be used for downstream analysis in RNA-seq studies, particularly in the context of SQANTI protein classification.

## Input files
- `sample1_cds.gtf` - CDS GTF file from the [07_make_cds_gtf module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_make_cds_gtf)
- `sample2_cds.gtf` - CDS GTF file from the [07_make_cds_gtf module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_make_cds_gtf)
- reference.gtf - GTF file from Gencode 

## Output files
- `condition1_exon.gtf` - Exon GTF file for condition 1
- `condition1_exons_only.gtf` - Exon-only GTF file for condition 1
- `condition2_exon.gtf` - Exon GTF file for condition 2
- `condition2_exons_only.gtf` - Exon-only GTF file for condition 2
- `gencode_exon.gtf` - Exon GTF file for GENCODE reference genome
- `gencode_exons_only.gtf` - Exon-only GTF file for GENCODE reference genome

## Required installations
Load modules (if on HPC) and create and activate `reference_tab` conda environment. <br />
```
module load apptainer/1.3.4
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda activate reference_tab
```
Load Docker (here using Apptainer). <br />
```
apptainer pull docker://gsheynkmanlab/pb-cds-gtf:latest
```
## Run rename CDS to exon from a SLURM script
```
sbatch 00_scripts/08_rename_cds_to_exon.sh
```
## Or run these commands.
Note, this is where the docker image lives on the Sheynkman lab server. If you are using a different server, you will need to change the path to the docker image. <br />
```
apptainer exec /project/sheynkman/dockers/LRP/pb-cds-gtf_latest.sif /bin/bash -c " \
  python 00_scripts/08_rename_cds_to_exon_multi.py \
  --sample1_gtf 07_make_cds_gtf/condition1_cds.gtf \
  --sample1_name 08_rename_cds_to_exon/condition1 \
  --sample2_gtf 07_make_cds_gtf/condition2_cds.gtf \
  --sample2_name 08_rename_cds_to_exon/condition2 \
  --reference_gtf /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
  --reference_name 08_rename_cds_to_exon/gencode \
  --num_cores 8 
"

conda deactivate 
module purge
```

## Proceed to [09_sqanti_protein module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/09_sqanti_protein)
