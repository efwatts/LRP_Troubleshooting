# 5 Prime Untranslated Regions
Intermediate step for protein classification. <br />
This module is comprised of three scripts that build on one another. <br />
Here is an AI generated summary of this step: <br />
> The `5' UTR` module is designed to analyze the 5' untranslated regions (UTRs) of transcripts in RNA-seq data. It consists of three scripts that work together to extract and classify 5' UTR information from GTF files. The first script retrieves exon chain strings for transcripts containing coding sequences (CDS), the second script classifies the 5' UTR status of transcripts based on their exon chains, and the third script merges the 5' UTR classification information with protein classification data. This module is essential for understanding the regulatory elements present in the 5' UTRs of transcripts and their potential impact on gene expression and translation.
## Input files
- `cds.gtf` - CDS GTF file from the [07_make_cds_gtf module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_make_cds_gtf)
- `gencode.annotation.gtf` - GTF file from Gencode. <br />
## ## Required installations
If running on Rivanna or other HPC, load required modules and create and activate conda environment. <br />
```
module load gcc/11.4.0
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda env create -f ./00_environments/utr.yml
conda activate utr
```

## Run 5' UTR from a SLURM script
```
sbatch 00_scripts/10_5p_utr.sh
```
## Or run these commands.
```
python 00_scripts/10_1_get_gc_exon_and_5utr_info.py \
--gencode_gtf /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
--odir 10_5p_utr

# condition 1
python 00_scripts/10_2_classify_5utr_status.py \
--gencode_exons_bed 10_5p_utr/gencode_exons_for_cds_containing_ensts.bed \
--gencode_exons_chain 10_5p_utr/gc_exon_chain_strings_for_cds_containing_transcripts.tsv \
--sample_cds_gtf 07_make_cds_gtf/condition1_cds.gtf \
--odir 10_5p_utr 

python 00_scripts/10_3_merge_5utr_info_to_pclass_table.py \
--name condition1 \
--utr_info 10_5p_utr/pb_5utr_categories.tsv \
--sqanti_protein_classification 09_sqanti_protein/condition1.sqanti_protein_classification.tsv \
--odir 10_5p_utr

# condition 2
python 00_scripts/10_2_classify_5utr_status.py \
--gencode_exons_bed 10_5p_utr/gencode_exons_for_cds_containing_ensts.bed \
--gencode_exons_chain 10_5p_utr/gc_exon_chain_strings_for_cds_containing_transcripts.tsv \
--sample_cds_gtf 07_make_cds_gtf/condition2_cds.gtf \
--odir 10_5p_utr 

python 00_scripts/10_3_merge_5utr_info_to_pclass_table.py \
--name condition2 \
--utr_info 10_5p_utr/pb_5utr_categories.tsv \
--sqanti_protein_classification 09_sqanti_protein/condition1.sqanti_protein_classification.tsv \
--odir 10_5p_utr

conda deactivate
module purge
```
## Proceed to [11_protein_classification module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/11_protein_classification)
