# Sqanti Protein
This is a [method previously developed by our group](https://github.com/sheynkman-lab/Long-Read-Proteogenomics/tree/main/modules/sqanti_protein) designed to classify the proteins found by the LRP using the [SQANTI3](https://github.com/ConesaLab/SQANTI3) naming conventions. It is an adaptation of the SQANTI3 script `sqanti3_qc.py`. <br />

Here is an AI generated summary of this step: <br />
> The `sqanti_protein.py` script is designed to classify proteins based on their coding potential and structural features. It takes as input a GTF file containing transcript annotations, a GTF file with CDS regions, an ORF database, and a reference GTF file. The script processes these inputs to generate a protein classification report, which includes information about the coding potential of the transcripts, their structural features, and their alignment to the reference genome. The resulting report can be used for downstream analysis in RNA-seq studies, particularly in the context of proteomics and functional genomics.
## Input files
- `condition1.transcript_exons_only.gtf` - transcript GTF file from the [08_rename_cds_to_exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/08_rename_cds_to_exon)
- `condition1.cds_renamed_exon.gtf` - CDS GTF file from the [08_rename_cds_to_exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/08_rename_cds_to_exon)
- `condition1_best_ORF.tsv` - ORF database from the [05_orf_calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling)
- `condition2.transcript_exons_only.gtf` - transcript GTF file from the [08_rename_cds_to_exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/08_rename_cds_to_exon)
- `condition2.cds_renamed_exon.gtf` - CDS GTF file from the [08_rename_cds_to_exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/08_rename_cds_to_exon)
- condition2_best_ORF.tsv - ORF database from the [05_orf_calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling)
- `gencode.transcript_exons_only.gtf` - transcript GTF file from the [08_rename_cds_to_exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/08_rename_cds_to_exon)
- `gencode.cds_renamed_exon.gtf` - CDS GTF file from the [08_rename_cds_to_exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/08_rename_cds_to_exon)

## Output files
- `condition1.sqanti_protein_classification.tsv` - SQANTI protein classification for condition 1
- `condition2.sqanti_protein_classification.tsv` - SQANTI protein classification for condition 2

## Required installations
Load modules (if on HPC) and create and activate `sqanti_protein` conda environment. <br />
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load apptainer/1.3.4
module load miniforge/24.3.0-py3.11
module load R/4.3.1 
module load perl/5.36.0 
module load star/2.7.9a 

conda env create -f ./00_environments/09_sqanti_protein.yml
conda activate sqanti_protein
```
## Run sqanti_protein from a SLURM script
```
sbatch 00_scripts/09_sqanti_protein.sh
```
## Or run these commands.
```
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/sequence/
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2

# condition 1
python 00_scripts/09_sqanti_protein.py \
08_rename_cds_to_exon/condition1.transcript_exons_only.gtf \
08_rename_cds_to_exon/condition1.cds_renamed_exon.gtf \
05_orf_calling/best_ORF_condition1.tsv \
08_rename_cds_to_exon/gencode.transcript_exons_only.gtf \
08_rename_cds_to_exon/gencode.cds_renamed_exon.gtf \
-d 09_sqanti_protein/ \
-p condition1

# condition 2
python 00_scripts/09_sqanti_protein.py \
08_rename_cds_to_exon/condition2.transcript_exons_only.gtf \
08_rename_cds_to_exon/condition2.cds_renamed_exon.gtf \
05_orf_calling/best_ORF_condition2.tsv \
08_rename_cds_to_exon/gencode.transcript_exons_only.gtf \
08_rename_cds_to_exon/gencode.cds_renamed_exon.gtf \
-d 09_sqanti_protein/ \
-p condition2

conda deactivate
module purge
```

## Proceed to [10_5p_utr module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/10_5p_utr)
