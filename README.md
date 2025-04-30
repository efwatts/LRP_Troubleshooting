# Long Read Proteogenomics Pipeline Development & Troubleshooting
Here is where I house updated scripts for the [Sheynkman Lab LRP pipeline](https://github.com/sheynkman-lab/Long-Read-Proteogenomics) &amp;. This repository is **VERY ACTIVELY** being modified. If you are using this as a guide, please contact Emily Watts (watts.emily.f@virginia.edu) for assistance. There may be updates happening that have not been pushed to this repository yet <br />
At this time, this pipeline can be run with multiple biological replicates for two conditions. It is not yet set up to run with multiple biological replicates for more than two conditions. <br />
I have not updated any of the mass spectrometry-dependent modules yet. We have been focused on the RNA-seq modules for the past ~2 years. <br />

If you are in the Sheynkman Lab, my most recent LRP run can be found [here](https://github.com/sheynkman-lab/Mohi_MDS_LRP). It contains all the correct file paths for Dockers and programs stored on Rivanna. <br />

## This repository is for me to house original files & scripts
I also want to add my own scripts & modify original scripts to reflect any updates that have happened since it was written. <br />
I have organized the modules with numbers indicating the order in which to run them. Modules that can be run at the same stage have the same numbers. <br />
I'm working on adding summaries to each step for an quick explanation of the scripts, as part of the purpose of this repository is to explain each module step by step. <br />

## Make file structure in your working directory to make this pipeline run easily by cloning this repository
The generic scripts in this repository assume that your directory is organized in this manner and that your raw data is in your working directory in a folder called `00_input_data`. <br />
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
