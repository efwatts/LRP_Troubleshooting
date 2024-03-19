# Long Read Proteogenomics Pipeline Learning & Troubleshooting
Learning the [Sheynkman Lab LRP pipeline](https://github.com/sheynkman-lab/Long-Read-Proteogenomics) &amp; troubleshooting automation

## This repository is for me to house original files & scripts
I also want to add my own scripts & modify original scripts to reflect any updates that have happened since it was written. <br />
I have organized the modules with numbers indicating the order in which to run them. Modules that can be run at the same stage have the same numbers.

## Make file structure in your working directory to make this pipeline run easily 
The generic scripts in this repository assume that your directory is organized in this manner and that your raw data is in your working directory in a folder called `00_input_data`
```
mkdir ./01_isoseq/
mkdir ./01_isoseq/filter/
mkdir ./01_isoseq/lima/
mkdir ./01_isoseq/refine/
mkdir ./01_isoseq/cluster/
mkdir ./01_isoseq/align/
mkdir ./01_isoseq/collapse/
mkdir ./01_reference_tables/
mkdir ./02_sqanti/
mkdir ./03_CPAT/
```
## Load modules and environment
If running on Rivanna (or other HPC), be sure to load required module listed in this repository <br />
Create a conda environment with required packages. For ease, all packages for this pipeline are in an environment called "LRP.env" that can be created with the environment file in this repository. It contains many packages and will take time to load. <br />
The conda environments currently work best if you use a different env for each module...unfortunately <br />

## The general flow of the pipeline (so far) is this
Iso-Seq --> SQANTI3 --> CPAT --> ORF Calling --> Refine --> Make CDS GTF file (skipped for now) --> Track Visualization

## The generic input files required (so far) are these <br />
- raw_reads.ccs.bam <br /> 
- primers.fasta <br />
- assembly_genome.fasta <br />
- annotated_genome.gtf <br />
- PG_reference_table.tsv <br />
- Human_Hexamer.tsv (this one is specific) <br />
- Human_logitModel.RData (also specific) <br />
