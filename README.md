# Long Read Proteogenomics Pipeline Development & Troubleshooting
Here is where I house updated scripts for the [Sheynkman Lab LRP pipeline](https://github.com/sheynkman-lab/Long-Read-Proteogenomics) &amp;. This repository is **VERY ACTIVELY** being modified. If you are using this as a guide, please contact Emily Watts (watts.emily.f@virginia.edu) for assistance. There may be updates happening that have not been pushed to this repository yet <br />
At this time, this pipeline can be run with multiple biological replicates for two conditions. It is not yet set up to run with multiple biological replicates for more than two conditions. <br />
I have not updated any of the mass spectrometry-dependent modules yet. We have been focused on the RNA-seq modules for the past ~2 years. <br />
In most use cases, I skip the following modules: `15_accession_mapping`, `15_MS_file_convert`, `16_Metamorpheus`, `17_novel_peptides`, `17_peptide_analysis`, and `17_protein_group_compare`. <br />

If you are in the Sheynkman Lab, my most recent LRP run can be found [here](https://github.com/sheynkman-lab/Mohi_MDS_LRP). It contains all the correct file paths for Dockers and programs stored on Rivanna. <br />

## Make file structure in your working directory to make this pipeline run easily by cloning this repository
The generic scripts in this repository assume that your directory is organized in this manner and that you are working from your working directory (ie, don't change directories at each step). <br />
If you are in the Sheynkman Lab, do not use a `00_input_data` folder. Instead, use the raw files in the directory `/project/sheynkman/raw_data/` and direct the scripts to these files (it saves space in our project storage). <br />
```
module load git-lfs/2.10.0
git clone https://github.com/efwatts/LRP_Troubleshooting.git
cd LRP_Troubleshooting
```

## Load modules and environment
Each module lists the required modules and either has a `.yml` file to create the environment needed (eventually all will have these) or instructs you on how to create the environment.

## Input files for running this pipeline <br />
If you have Kinnex data, which is now the standard, these are the files you will need. If you have older PacBio data, you will need to run a few earlier steps in the [Iso-Seq pipeline](https://github.com/PacificBiosciences/pbbioconda) to be ready for the LRP pipeline. <br />
- raw_reads.flnc.bam from your PacBio data <br /> 
- from [Gencode](https://www.gencodegenes.org/):
  - gencode_gtf - Comprehensive gene annotation (regions: CHR) `gencode.v46.annotation.gtf` <br />
  - gencode_transcript_fasta - Protein-coding transcript sequences (regions: CHR) `gencode.v46_pc_transcripts.fa` <br />
  - gencode_translation_fasta - Protein-coding transcript translation sequences (regions: CHR) `gencode.v46_pc_translations.fa` <br />
  - genome_fasta - Genome sequence, primary assembly (GRCh38) (regions: PRI) `GRCh38.primary_assembly.genome.fa` <br />
- Human_Hexamer.tsv reference file <br />
- Human_logitModel.RData reference file <br />
- Optional: kallisto.tsv from your data <br />
- Optional (for Modules 15-17): MS search files.raw <br />
- Optional (for Modules 16-17): UniProt reviewed.fasta from [UniProt database](https://www.uniprot.org/help/downloads) <br />

# Pipeline Structure <br />
I typically use this README.md file to keep track of the modules I have run and the order I have run them in. <br />
I also use it to make notes on the particular LRP run I am working on. <br />
If you clone this repository, you can erase the contents of this file and use it for your own notes. <br />
A typical README.md file in my working directory looks like this: <br />

# Project Name LRP
This repository is being used to applyf the Long Read Proteogenomics pipeline to my project. <br />
Include important information about your dataset here. <br />
You can also include information about where your data is stored and how to access it. <br />
Be sure to include the GENCDOE version you are using. <br />

## Clone the LRP repository and rename the directory to your project name
```
module load git-lfs/2.10.0
git clone https://github.com/efwatts/LRP_Troubleshooting.git

rename 's/^LRP_Troubleshooting$/project_name/' LRP_Troubleshooting
cd project_name
```
I typically load these modules at the beginning of a run, because my environment is prepared to do minor data manipulation outside of the LRP pipeline. <br />
```
module load gcc/11.4.0 openmpi/4.1.4 python/3.11.4 miniforge/24.3.0-py3.11 samtools/1.17 R/4.5.0
```
## 01 - Iso-Seq
```
sbatch 00_scripts/01_isoseq.sh
```
## 01 - Make reference tables
```
sbatch 00_scripts/01_make_reference_tables.sh
```
## 02 - SQANTI
```
sbatch 00_scripts/02_sqanti.sh
```
## 02 - Make gencode database
```
sbatch 00_scripts/02_make_gencode_database.sh
```
## 03 - Filter SQANTI
```
sbatch 00_scripts/03_filter_sqanti.sh
```
## 04 - CPAT
```
sbatch 00_scripts/04_cpat.sh
```
## 04 - Transcriptome Summary
```
sbatch 00_scripts/04_transcriptome_summary.sh
```
## 05 - ORF Calling
This is where we are splitting the two conditions. <br />
```
sbatch 00_scripts/05_orf_calling.sh
```
## 06 - Refine ORF Database
```
sbatch 00_scripts/06_refine_orf_database.sh
```
## 07 - Make CDS GTF
```
sbatch 00_scripts/07_make_cds_gtf.sh
```
## 08 - Rename CDS to Exon
```
sbatch 00_scripts/08_rename_cds_to_exon.sh
```
## 09 - SQANTI Protein
```
sbatch 00_scripts/09_sqanti_protein.sh
```
## 10 - 5' UTR
```
sbatch 00_scripts/10_5p_utr.sh
```
## 11 - Protein Classification
```
sbatch 00_scripts/11_protein_classification.sh
```
## 12 - Protein Gene Rename
```
sbatch 00_scripts/12_protein_gene_rename.sh
```
## 13 - Protein Filter
```
sbatch 00_scripts/13_protein_filter.sh
```
## 14 - Protein Hybrid Database
```
sbatch 00_scripts/14_protein_hybrid_database.sh
```
## 17 - Track Visualization
```
sbatch 00_scripts/17_track_visualization.sh
```
## 18 - SUPPA
```
sbatch 00_scripts/18_suppa.sh
```
## 19 - LRP Result Summary
Make gene counts for the edgeR analysis. <br />
```
python 00_scripts/01_isoseq_gene_counts.py 01_isoseq/collapse/merged.collapsed.flnc_count.txt 01_isoseq/gene_level_counts.txt
```
Now run `19_LRP_summary/edgeR.R` to get the edgeR results required for the next script. <br />
```
Rscript 19_LRP_summary/edgeR.R
```
Now run the LRP summary script to get the final results. <br />
```
sbacth 00_scripts/19_LRP_summary.sh
```
## 20 - DTE, DGE, and DTU analysis
These are in an R script that I typically run in RStudio, but you can also run it like this. <br />
```
Rscript 00_scripts/20_DTE_DGE_DTU.R
```