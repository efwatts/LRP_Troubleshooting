# 5 Prime Untranslated Regions
This module is comprised of three scripts that build on one another. <br />

_Input:_ <br />
- cds.gtf (from [Make CDS GTF module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/06_make_cds_gtf))
- gencode.annotation.gtf (from [Gencode](https://www.gencodegenes.org/))

_Intermediate files:_
- gc_exon_chain_strings_for_cds_containing_transcripts.tsv
- gencode_exons_for_cds_containing_ensts.bed
- gencode_exons_for_cds_containing_ensts.bed_merged.bed
- pb_5utr_categories.tsv

_Output:_
- sqanti_protein_classification_w_5utr_info.tsv

## Run sqanti_protein
If running on Rivanna or other HPC, load required modules.
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11
```
Create, populate, and activate conda environment. <br />
```
conda create -n utr
conda activate utr
conda install pandas
pip install --upgrade bottleneck
```
Run the scripts!
```
python ./00_scripts/09_1_get_gc_exon_and_5utr_info.py \
--gencode_gtf ./00_input_data/gencode.v35.annotation.canonical.gtf \
--odir ./09_5p_utr

python ./00_scripts/09_2_classify_5utr_status.py \
--gencode_exons_bed ./09_5p_utr/gencode_exons_for_cds_containing_ensts.bed \
--gencode_exons_chain ./09_5p_utr/gc_exon_chain_strings_for_cds_containing_transcripts.tsv \
--sample_cds_gtf ./06_make_cds_gtf/jurkat_cds.gtf \
--odir ./09_5p_utr 

python ./00_scripts/09_3_merge_5utr_info_to_pclass_table.py \
--name jurkat \
--utr_info ./09_5p_utr/pb_5utr_categories.tsv \
--sqanti_protein_classification ./08_sqanti_protein/jurkat.sqanti_protein_classification.tsv \
--odir ./09_5p_utr

conda deactivate
module purge
```
