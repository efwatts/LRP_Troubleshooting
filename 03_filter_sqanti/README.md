# Filter SQANTI
Filter SQANTI3 results based on these criteria: 
- protein coding only
  - PB transcript aligns to a GENCODE-annotated protein coding gene.
- percent A downstream
  - perc_A_downstreamTTS : percent of genomic "A"s in the downstream 20 bp window. If this number if high (> 80%), the 3' end have arisen from intra-priming during the RT step
- RTS stage
  - RTS_stage: TRUE if one of the junctions could be an RT template switching artifact.
- Structural Category
  - keep only transcripts that have a isoform structural category of:
    - novel_not_in_catalog
    - novel_in_catalog
    - incomplete-splice_match
    - full-splice_match


_Input:_ <br />
- classification.txt (from [SQANTI3 module](https://github.com/efwatts/LRP_Troubleshooting/blob/main/02_SQANTI/README.md))
- corrected.fasta (from [SQANTI3 module](https://github.com/efwatts/LRP_Troubleshooting/blob/main/02_SQANTI/README.md))
- corrected.gtf (from [SQANTI3 module](https://github.com/efwatts/LRP_Troubleshooting/blob/main/02_SQANTI/README.md))
- protein_coding_genes.txt (from [Reference Tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))
- ensg_gene.txt (from [Reference Tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))

_Intermediate files:_
- filtered_classification.tsv
- filtered_corrected.fasta
- filtered_corrected.gtf

_Output:_
- classification.5degfilter.tsv
- corrected.5degfilter.fasta
- corrected.5d3gfilter.gtf

## Filter SQANTI
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
conda create -n sqanti_filter
conda activate sqanti_filter
conda install pandas
pip install argparse
pip install gtfparse
```
Run the scripts!
```
python ./00_scripts/03_filter_sqanti.py \
    --sqanti_classification ./02_sqanti/output/jurkat_classification.txt \
    --sqanti_corrected_fasta ./02_sqanti/output/jurkat_corrected.fasta \
    --sqanti_corrected_gtf ./02_sqanti/output/jurkat_corrected.gtf \
    --protein_coding_genes ./01_reference_tables/protein_coding_genes.txt \
    --ensg_gene ./01_reference_tables/ensg_gene.tsv \
    --filter_protein_coding yes \
    --filter_intra_polyA yes \
    --filter_template_switching yes \
    --percent_A_downstream_threshold 95 \
    --structural_categories_level strict \
    --minimum_illumina_coverage 3 

python ./00_scripts/03_collapse_isoforms.py \
    --name jurkat \
    --sqanti_gtf ./03_filter_sqanti/filtered_jurkat_corrected.gtf \
    --sqanti_fasta ./03_filter_sqanti/filtered_jurkat_corrected.fasta

python ./00_scripts/03_collapse_classification.py \
    --name jurkat \
    --collapsed_fasta ./03_filter_sqanti/jurkat_corrected.5degfilter.fasta \
    --classification ./03_filter_sqanti/filtered_jurkat_classification.tsv

conda deactivate
module purge
```

## Proceed to [CPAT module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_CPAT)
