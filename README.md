# Long Read Proteogenomics Pipeline Learning & Troubleshooting
Learning the [Sheynkman Lab LRP pipeline](https://github.com/sheynkman-lab/Long-Read-Proteogenomics) &amp; troubleshooting automation. It is **VERY ACTIVELY** being modified. If you are using this as a guide, please contact Emily Watts (watts.emily.f@virginia.edu) for assistance.  

## This repository is for me to house original files & scripts
I also want to add my own scripts & modify original scripts to reflect any updates that have happened since it was written. <br />
I have organized the modules with numbers indicating the order in which to run them. Modules that can be run at the same stage have the same numbers.

## Make file structure in your working directory to make this pipeline run easily 
The generic scripts in this repository assume that your directory is organized in this manner and that your raw data is in your working directory in a folder called `00_input_data`
```
mkdir ./00_environments/
mkdir ./00_input_data/
mkdir ./00_scripts/
mkdir ./01_isoseq/
mkdir ./01_isoseq/01_filter/
mkdir ./01_isoseq/02_lima/
mkdir ./01_isoseq/03_refine/
mkdir ./01_isoseq/04_cluster/
mkdir ./01_isoseq/05_align/
mkdir ./01_isoseq/06_collapse/
mkdir ./01_reference_tables/
mkdir ./02_make_gencode_database/
mkdir ./02_sqanti/
mkdir ./03_filter_sqanti/
mkdir ./04_CPAT/
mkdir ./04_six_frame_translation/
mkdir ./04_transcriptome_summary/
mkdir ./05_orf_calling/
mkdir ./06_refine_orf_database/
mkdir ./07_accession_mapping/
mkdir ./07_make_cds_gtf/
mkdir ./08_rename_cds_to_exon/
mkdir ./09_sqanti_protein/
mkdir ./10_5p_utr/
mkdir ./11_protein_classification/
mkdir ./12_protein_gene_rename/
mkdir ./13_protein_filter/
mkdir ./14_protein_hybrid_database/
mkdir ./15_MS_file_convert/
mkdir ./16_MetaMorpheus/
mkdir ./16_MetaMorpheus/gencode/
mkdir ./16_MetaMorpheus/hybrid/
mkdir ./16_MetaMorpheus/filtered/
mkdir ./16_MetaMorpheus/refined/
mkdir ./17_peptide_analysis/
mkdir ./17_track_visualization/
mkdir ./17_protein_group_comparison/
mkdir ./17_novel_peptides/
```

## Load modules and environment
Each module lists the required modules and either has a `.yml` file to create the environment needed (eventually all will have these) or instructs you on how to create the environment.

## Input files for running this pipeline <br />
- raw_reads.ccs.bam from your PacBio data <br /> 
- primers.fasta from your PacBio data <br />
- from [Gencode](https://www.gencodegenes.org/):
  - gencode_gtf - Comprehensive gene annotation (regions: CHR) `gencode.v38.annotation.gtf` <br />
  - gencode_transcript_fasta - Protein-coding transcript sequences (regions: CHR) `gencode.v38_pc_transcripts.fa` <br />
  - gencode_translation_fasta - Protein-coding transcript translation sequences (regions: CHR) `gencode.v38_pc_translations.fa` <br />
  - genome_fasta - Genome sequence, primary assembly (GRCh38) (regions: PRI) `GRCh38.primary_assembly.genome.fa` <br />
- Human_Hexamer.tsv reference file <br />
- Human_logitModel.RData reference file <br />
- Optional: kallisto.tsv from your data <br />
- Optional (for Modules 15-17): MS search files.raw <br />
- Optional (for Modules 16-17): UniProt reviewed.fasta from [UniProt database](https://www.uniprot.org/help/downloads) <br />
