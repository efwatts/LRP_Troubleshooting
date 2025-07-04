# Filter SQANTI
This module filters SQANTI3 results based on the following criteria:
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
    - full-splice_match <br />
  
**Please note: if you are using mouse data, use the `03_filter_sqanti_mouse.py` script at this step.** <br />

Here is an AI-generated flowchart describing how the multiple scripts in this module relate to each other:
<pre>
```
                    SQANTI3 Output
                 ┌──────────────────────┐
                 │ MDS_classification.txt
                 │ MDS_corrected.gtf
                 │ MDS_corrected.fasta
                 └──────────────────────┘
                            │
                            ▼
         [03_filter_sqanti_mouse.py] — filter by structure, coverage, etc.
                            │
                            ▼
                 ┌──────────────────────────────┐
                 │ filtered_MDS_classification.txt
                 │ filtered_MDS_corrected.gtf
                 │ filtered_MDS_corrected.fasta
                 └──────────────────────────────┘
                            │
                            ▼
             [03_collapse_isoforms.py] — remove redundant isoforms
                            │
                            ▼
                 ┌────────────────────────────────────┐
                 │ MDS_corrected.5degfilter.fasta      │
                 │ MDS_corrected.5degfilter.gff        │
                 │ dropout/*.gff and *.fasta           │
                 └────────────────────────────────────┘
                            │
                            ▼
   [03_collapse_classification.py] — update classification to retained isoforms
                            │
                            ▼
                 ┌────────────────────────────────────┐
                 │ MDS_classification.5degfilter.tsv   │
                 └────────────────────────────────────┘
                            │
                            ▼
   [03_filter_sqanti_raw_counts.py] — generate raw FL count matrix
                            ▼
                 ┌────────────────────────────────────┐
                 │ MDS_filtered_raw_counts.tsv         │
                 └────────────────────────────────────┘
```
</pre>


## Input files
- `classification.txt` - SQANTI3 classification file
- `corrected.fasta` - SQANTI3 corrected FASTA file
- `corrected.gtf` - SQANTI3 corrected GTF file
- `protein_coding_genes.txt` - protein coding genes file
- `ensg_gene.txt` - ENSEMBL gene file

## Required installations
Load modules (if on HPC) and create and activate conda environment. <br />
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load miniforge/24.3.0-py3.11

conda create -n sqanti_filter
conda activate sqanti_filter
```
## Run Filter SQANTI3 from a SLURM script
```
sbatch 00_scripts/03_filter_sqanti.sh
```
## Or run these commands.
Note: you have to add SQANTI3 cDNA_Cupcake directory to your path. <br />
```
chmod +x /project/sheynkman/programs/SQANTI3-5.2/utilities/gtfToGenePred
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/sequence/
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/

python 00_scripts/03_filter_sqanti.py \
    --sqanti_classification 02_sqanti/sample_classification.txt \
    --sqanti_corrected_fasta 02_sqanti/sample_corrected.fasta \
    --sqanti_corrected_gtf 02_sqanti/sample_corrected.gtf \
    --protein_coding_genes 01_reference_tables/protein_coding_genes.txt \
    --ensg_gene 01_reference_tables/ensg_gene.tsv \
    --filter_protein_coding yes \
    --filter_intra_polyA yes \
    --filter_template_switching yes \
    --percent_A_downstream_threshold 95 \
    --structural_categories_level strict \
    --minimum_illumina_coverage 3 \
    --output_dir 03_filter_sqanti/speed_test

python 00_scripts/03_collapse_isoforms.py \
    --name sample \
    --sqanti_gtf 03_filter_sqanti/filtered_sample_corrected.gtf \
    --sqanti_fasta 03_filter_sqanti/filtered_sample_corrected.fasta \
    --output_dir 03_filter_sqanti/speed_test

python 00_scripts/03_collapse_classification.py \
    --name sample \
    --collapsed_fasta 03_filter_sqanti/sample_corrected.5degfilter.fasta \
    --classification 03_filter_sqanti/filtered_sample_classification.txt \
    --output_folder 03_filter_sqanti/sample

conda deactivate
module purge
```

## Proceed to [CPAT module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_CPAT)
