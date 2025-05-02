# Make CDS GTF
This module is used to create a CDS (coding sequence) GTF file from the previous few steps' ORF output. The CDS GTF file is used for downstream analysis, such as protein classification and functional annotation. <br />

Here is an AI generated summary of this step: <br />
> The `make_cds_gtf.py` script is designed to create a CDS (coding sequence) GTF file from the output of the ORF calling step. It takes as input the filtered GTF file, the refined ORF database, and the transcriptome summary files. The script processes these inputs to generate a GTF file that contains information about the coding sequences of the transcripts, including their start and stop codons, exon coordinates, and gene annotations. The resulting CDS GTF file can be used for downstream analysis in RNA-seq studies.
## Input files
- `corrected.5degfilter.gff` - filtered GTF file from the [03_filter_sqanti module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti)
- `best_ORF.tsv` - ORF database from the [05_orf_calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling)
- `pb_gene.tsv` - PB gene file from the [04_transcriptome_summary module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_transcriptome_summary)
- `refined_orfs.tsv` - refined ORF database from the [06_refine_orf_database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_refine_orf_database)

## Required installations
Load modules (if on HPC) and create and activate conda environment. <br />
```
module load apptainer/1.2.2
module load gcc/11.4.0
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda env create -f ./00_environments/07_make_cds_gtf.yml
conda activate make-cds-gtf
```
Load Docker (here using Apptainer). <br />
```
apptainer pull docker://gsheynkmanlab/pb-cds-gtf:latest
```

## Run CDS GTF from a SLURM script
```
sbatch 00_scripts/07_make_cds_gtf.sh
```
## Or run these commands.
Note, this is where the docker image lives on the Sheynkman lab server. If you are using a different server, you will need to change the path to the docker image. <br />
```
# condition1
# Command to open the container & run script

apptainer exec /project/sheynkman/dockers/LRP/pb-cds-gtf_latest.sif /bin/bash -c " \
    python 00_scripts/07_make_pacbio_cds_gtf.py \
    --sample_gtf 03_filter_sqanti/sample_corrected.5degfilter.gff \
    --agg_orfs 06_refine_orf_database/condition1_0_orf_refined.tsv \
    --refined_orfs 05_orf_calling/best_ORF_condition1.tsv \
    --pb_gene 04_transcriptome_summary/pb_gene.tsv \
    --output_cds 07_make_cds_gtf/condition1_cds.gtf
"

# condition2
# Command to open the container & run script

apptainer exec /project/sheynkman/dockers/LRP/pb-cds-gtf_latest.sif /bin/bash -c " \
    python 00_scripts/07_make_pacbio_cds_gtf.py \
    --sample_gtf 03_filter_sqanti/sample_corrected.5degfilter.gff \
    --agg_orfs 06_refine_orf_database/condition2_0_orf_refined.tsv \
    --refined_orfs 05_orf_calling/best_ORF_condition2.tsv \
    --pb_gene 04_transcriptome_summary/pb_gene.tsv \
    --output_cds 07_make_cds_gtf/condition2_cds.gtf
"

conda deactivate
module purge
```
## Proceed to [08_rename_cds_to_exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/08_rename_cds_to_exon)
