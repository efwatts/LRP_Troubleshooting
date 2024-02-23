# LRP_Troubleshooting
learning LRP pipeline &amp; troubleshooting automation

## This repository is for me to house original files & scripts
I also want to add my own scripts & modify original scripts to reflect any updates that have happened since it was written.

## Load modules and environment
If running on Rivanna (or other HPC), be sure to load required module listed in this repository <br />
Create a conda environment with required packages. For ease, all packages for this pipeline are in an environment called "LRP.env" that can be created with the environment file in this repository. It contains many packages and will take time to load. <br />
The conda environments currently work best if you use a different env for each module...unfortunately <br />

## The general flow of the pipeline (so far) is this
Iso-Seq --> SQANTI3 --> CPAT --> ORF Calling --> Refine

## The generic input files required (so far) are these <br />
- raw_reads.ccs.bam <br /> 
- primers.fasta <br />
- assembly_genome.fasta <br />
- annotated_genome.gtf <br />
- PG_reference_table.tsv <br />
- Human_Hexamer.tsv (this one is specific) <br />
- Human_logitModel.RData (also specific) <br />
